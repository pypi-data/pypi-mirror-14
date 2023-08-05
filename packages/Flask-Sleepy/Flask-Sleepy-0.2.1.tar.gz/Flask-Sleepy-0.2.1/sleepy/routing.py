from flask import request, Response
from werkzeug.exceptions import abort

from sleepy.adapter import MarshmallowSchemaMixin, SerializationException, SQLAModelMixin


class RouteProxy(object):
    """
    Abstract class for creating extra routes on view classes like with the @route decorated
    and the ListAttributeAccessor.
    """

    http_methods = None
    view_cls = None
    view_kwargs = None

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def register(self, app, view_cls, url, name, methods=None, **view_kwargs):
        """
        Register the url rules for this proxy?
        :param app: the app to register the rules on
        :param view_cls: the view_cls from which the route will 'inherit'
        :param url: the url(-prefix) on which the proxy should be defined
        :param name: the name under which the rule should be defined
        :param methods: the http methods by wich the url should be reachable
        :param view_kwargs: the arguments for the view class constructor (currently not used,
        but might come in handy for end users). Note that the view instance is contructed on each request.
        """
        methods = methods if methods else self.http_methods

        self.view_cls = view_cls
        self.view_kwargs = view_kwargs

        self.add_url_rule(app,
                          self,
                          url=url,
                          name=name,
                          methods=methods)


    def add_url_rule(self, app, f, url, name, methods):
        try:
            app.add_url_rule(url,
                             view_func=f,
                             methods=methods,
                             endpoint=name)
        except AssertionError as err:
            raise Exception("Flask doesn't like url rule named {}: {} -> {}. "
                            "Did you put two route decorators on the same method and not give "
                            "them explicit and distinct names?".format(name, url, f)) from err


class ListAttributeAccessor(RouteProxy, SQLAModelMixin, MarshmallowSchemaMixin):
    """
    Can be used as an attribute of a sleepyview to automatically define
    index (GET /parent/1/children/), create (POST /parent/1/children/) and
    remove (DELETE /parent/1/children/1/) actions for the relationship between
    the model and one of its one-to-many or many-to-many relationships.

    Note that the POST /parent/1/children opertion by default takes a body like {"id":1} to add
    child 1 to the relation and does not create Child records itself.

    Usage:

    class ParentView(SleepyView):
        model = Parent
        schema = ParentSchema

        # allow acces to the 'children' attribute of the Parent model, which is a list Child
        # instances and should be marshalled using ChildSchema
        children = ListAttributeAccessor("children", Child, ChildSchema)
    """
    def __init__(self, attr_name, attr_model, schema, id_key="id"):
        """
        Construct the accessor. To be called at load time.
        :param attr_name: name of the list attribute (must return a list, not an sqla query object! (for now?))
        :param attr_model: model of the attribute for the lookups
        :param schema: schema for the marshalling (no unmarshalling for now, see note in class doc)
        :param id_key:
        """
        self.attr_name = attr_name
        self.schema = schema
        self.model = attr_model
        self.id_key = id_key
        # todo: add functionality to specify the url postfix (default remains .../attr_name/)


    def register(self, app, view_cls, url_prefix, view_name, methods=None, **view_kwargs):
        """
        Register the url rules for this proxy?
        :param app: the app to register the rules on
        :param view_cls: the view class
        :param url-prefix: the url-prefix) on which the proxy should be defined
        :param view_name: the name of the endpoint.
        :param methods: the http methods by wich the url should be reachable
        :param view_kwargs: the arguments for the view class constructor (currently not used,
        but might come in handy for end users). Note that the view instance is contructed on each request.
        """
        if not methods:
            index_methods = ("GET", "POST", )
            entity_methods = ("DELETE", )
        else:
            index_methods = methods
            entity_methods = methods  # TODO: actually make routes configurable in some way

        url = "{}<int:obj_id>/{}/".format(url_prefix, self.attr_name)
        name = "{}.{}".format(view_name, self.attr_name)

        super().register(app, view_cls, url, name, methods=index_methods, **view_kwargs)

        self.add_url_rule(app, self, url="{}<int:attr_id>/".format(url), name=name, methods=entity_methods)


    def id_from_request(self):
        if self.id_key not in request.json:
            raise SerializationException("Missing {} key in request body".format(self.id_key))

        return request.json[self.id_key]

    def attr_from_obj(self, obj):
        attr = getattr(obj, self.attr_name, None)  # get the attribute of that object we want to access
        if attr is None:  # attr is allowed to be an empty list, though.
            abort(404)

        return attr



    def __call__(self, obj_id, *args, **kwargs):
        """
        Execute the request. This method acts as a kind of dispatch_request.
        """
        view_instance = self.view_cls(**self.view_kwargs)  # construct the view instance on the fly

        obj = view_instance.get_obj(obj_id)  # get the object we're talking about

        if request.method == 'GET':
            return Response(response=self.marshall_objs(self.get_all_in_relation(obj)),
                            content_type="application/json")
        elif request.method == 'POST':
            self.add_to_relation(obj, self.id_from_request())
            return "", 204
        elif request.method == 'DELETE':
            if "attr_id" not in kwargs:
                abort(405)  # not allowed to delete whole relation at once.
            else:
                self.delete_from_relation(obj, kwargs["attr_id"])
                return "", 204

        else:
            abort(405)

    def validate_before_adding(self, obj):
        """
        This method, which does nothing by default, is executed right before an object is added to the relation and
        should raise an exception or flask.abort if this object may not be added to the relation.
        """
        pass

    def add_to_relation(self, obj, attr_id):
        """
        Add the list attribute element to the relation with the object
        :param obj: the sqla model instance of which the attribute will be added to
        :param attr_id: the db id of the list atribute element to be added
        """""
        try:
            self.session.begin(subtransactions=True)
            attr_obj_to_be_added = self.get_obj(attr_id)
            self.validate_before_adding(obj)  # should abort or raise when something isn't valid.
            attr = self.attr_from_obj(obj)
            attr.append(attr_obj_to_be_added)
            self.session.commit()
        except:
            self.session.rollback()
            abort(409, message="This scheduling conflicts with a recently added scheduling.")

    def delete_from_relation(self, obj, attr_id):
        """
        Remove the list attribute element from the relation with the object
        :param obj: the sqla model instance of which the attribute will be removed from
        :param attr_id: the db id of the list atribute element to be removed
        """""
        attr_obj_to_be_deleted = self.get_obj(attr_id)
        attr = self.attr_from_obj(obj)
        attr.remove(attr_obj_to_be_deleted)
        self.session.commit()

    def get_all_in_relation(self, obj):
        """
        Get all elements of the list attribute.
        :param obj: the sqla model instance of which the attribute will be read
        :return: all elements of the list attribute.
        """
        return self.attr_from_obj(obj)



class RouteDecorated(RouteProxy):

    def __init__(self, meth, url_postfix, methods=("GET", ), name=None):
        """
        Decorator for custom routes on sleepyviews.

        :param url_postfix: What is appended to the url prefix of the view the decorated method is defined on.
        :param methods: Allowed http methods on this url.
        """

        self.routes = [(url_postfix, methods, name)]

        self.http_methods = tuple(methods)
        self.meth = meth
        self.__name__ = meth.__name__


    def add_route(self, url_postfix, methods=("GET", ), name=None):
        self.routes.append((url_postfix, methods, name, ))

    def __call__(self, *args, **kwargs):

        view_instance = self.view_cls(**self.view_kwargs)  # construct the view instance on the fly
        return self.meth(view_instance, *args, **kwargs)


    def register(self, app, view_cls, url_prefix, view_name, methods=None, **view_kwargs):
        """
        Register the url rules for this proxy?
        :param app: the app to register the rules on
        :param view_cls: the view_cls from which the route will 'inherit'
        :param url_prefix: the url-prefix) on which the proxy should be defined
        :param name: the name under which the rule should be defined
        :param methods: the http methods by wich the url should be reachable. Unused here as they are defined
        each time the @route decorator is used.
        :param view_kwargs: the arguments for the view class constructor (currently not used,
        but might come in handy for end users). Note that the view instance is contructed on each request.
        """
        self.view_cls = view_cls
        self.view_kwargs = view_kwargs

        for url_postfix, methods, name in self.routes:

            self.add_url_rule(app,
                              self,
                              url="{}{}".format(url_prefix, url_postfix),
                              name="{}.{}".format(view_name, name),
                              methods=methods)


def route(url_postfix, methods=("GET", ), name=None):
    """
    Decorator for custom routes to methods on view classes.
    :param url_postfix: the url_postifx for the url (prefix is the one defined when registering the view class)
    :param methods: the http methods expected by the method
    :param name: the name for the url rule. (if not set, the name of the method is used)
    :return:
    """

    def wrapper(f):
        view_name = name if name else f.__name__
        if isinstance(f, RouteDecorated):  # we need one RouteDecorated object per method.
            f.add_route(url_postfix, methods, view_name)
            return f
        else:
            return RouteDecorated(f, url_postfix, methods, view_name if view_name else f.__name__)

    return wrapper