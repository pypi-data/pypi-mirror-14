from flask import request, Response
from werkzeug.exceptions import abort

from sleepy.adapter import MarshmallowSchemaMixin, SerializationException, SQLAModelMixin


__author__ = 'robin'


class RouteProxy(object):

    http_methods = None
    view_cls = None
    view_kwargs = None

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def register(self, app, view_cls, url, name, methods=None, **view_kwargs):
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
    def __init__(self, attr_name, attr_model, schema,
                 http_methods=("GET", "POST", "DELETE"),
                 id_key="id"):

        self.attr_name = attr_name
        self.schema = schema
        self.http_methods = http_methods
        self.model = attr_model
        self.id_key = id_key
        # todo: add functionality to specify the url postfix (default remains .../attr_name/)


    def id_from_request(self):
        if self.id_key not in request.json:
            raise SerializationException("Missing {} key in request body".format(self.id_key))

        return request.json[self.id_key]

    def attr_from_obj(self, obj):
        attr = getattr(obj, self.attr_name, None)  # get the attribute of that object we want to access
        if attr is None: # attr is allowed to be an empty list, though.
            abort(404)

        return attr

    def register(self, app, view_cls, url, name, **view_kwargs):
        super().register(app, view_cls, url, name, methods=("GET", "POST", ), **view_kwargs)

        self.add_url_rule(app, self, url="{}<int:attr_id>/".format(url), name=name, methods=("DELETE", ))

    def __call__(self, obj_id, *args, **kwargs):

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
        pass

    def add_to_relation(self, obj, attr_id):
        attr_obj_to_be_added = self.get_obj(attr_id)
        self.validate_before_adding(obj) # should abort or raise when something isn't valid.
        attr = self.attr_from_obj(obj)
        attr.append(attr_obj_to_be_added)
        self.session.commit()

    def delete_from_relation(self, obj, attr_id):
        attr_obj_to_be_deleted = self.get_obj(attr_id)
        attr = self.attr_from_obj(obj)
        attr.remove(attr_obj_to_be_deleted)
        self.session.commit()

    def get_all_in_relation(self, obj):
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
        self.__name__ = name
        self.meth = meth


    def add_route(self, url_postfix, methods=("GET", ), name=None):
        self.routes.append((url_postfix, methods, name, ))

    def __call__(self, *args, **kwargs):

        view_instance = self.view_cls(**self.view_kwargs)  # construct the view instance on the fly
        return self.meth(view_instance, *args, **kwargs)


    def register(self, app, view_cls, url_prefix, **view_kwargs):
        self.view_cls = view_cls
        self.view_kwargs = view_kwargs

        for url_postfix, methods, name in self.routes:

            self.add_url_rule(app,
                              self,
                              url="{}{}".format(url_prefix, url_postfix),
                              name=name,
                              methods=methods)


def route(url_postfix, methods=("GET", ), name=None):
    def wrapper(f):
        view_name = name if name else f.__name__
        if isinstance(f, RouteDecorated):
            f.add_route(url_postfix, methods, view_name)
            return f
        else:
            return RouteDecorated(f, url_postfix, methods, view_name if view_name else f.__name__)

    return wrapper