from flask import Response, request
from flask.views import MethodView

import functools

from sleepy.adapter import SQLAModelAdapter, MarshmallowSchemaSerializer, SerializationException


class Sleepy(object):
    app = None
    db = None

    def __init__(self, app=None, db=None):

        """
        Initialize the Sleepy application. If you're  using this directly you're not using
        an app factory and you're a bad person.
        :param app: A flask app
        :param db: A Flask-SQLALchemy object
        """
        self.init_app(app, db)

    def init_app(self, app, db):
        """
        Initialize the Sleepy application.
        :param app: A flask app
        :param db: A Flask-SQLALchemy object
        """
        self.app = app
        self.db = db

    def add_endpoint(self, view_cls, url_prefix=None, name_prefix=None, pk_type='int', session=None, **kwargs):

        """
        Register a sleepy view with the application.

        :param view_cls: The Sleepy view class. This will be instantiated with remaining kwargs.
        :param url_prefix: The url prefix for the rule. If not specified, the url_prefix defined on
        the view class is used.
        :param name_prefix: The name prefix for the view. If not specified, the name_prefix defined on
        the view class is used.
        :param pk_type: The type of primary key of this model. Please just use ints, which are the default.
        :param session: An SQLAlchemy session. If not specified, a session is created using the db object passed during
        initialization.
        :param kwargs: Arguments passed to the view's constructor on creation.
        """
        if url_prefix:
            pass
        elif view_cls.url_prefix:
            url_prefix = view_cls.url
        else:
            raise Exception("No url prefix set for endpoint {}.".format(view_cls.__class__.__name__))

        if name_prefix:
            pass
        elif view_cls.name_prefix:
            name_prefix = view_cls.name_prefix
        else:
            raise Exception("No url name prefix set for endpoint {}.".format(view_cls.__class__.__name__))

        view_name = "{}_endpoint".format(name_prefix)

        if not session:
            session = self.db.session

        view_func = view_cls.as_view(name=view_name, session=session, **kwargs)

        # The index, allowing for the obj_id not to be provided
        # so we can use this for GET /thing/ and GET /thing/id/
        self.app.add_url_rule(url_prefix,
                              defaults={"obj_id": None},
                              view_func=view_func, methods=['GET', ])

        # url rule for creating an object by POSTing to /thing/
        self.app.add_url_rule(url_prefix,
                              view_func=view_func,
                              methods=['POST', ])

        # url rule for editing, getting and deleting an obj with the given id
        # by GETing, PUTing and DELETEing to /thing/id/
        self.app.add_url_rule('%s<%s:%s>/' % (url_prefix, pk_type, "obj_id"),
                              view_func=view_func,
                              methods=['GET', 'PUT', 'DELETE'])


        # find the methods decorated with routes and loop through their rule cache (see the route decorator
        # below for an explantation)
        for attr_name in dir(view_cls):
            meth = getattr(view_cls, attr_name)
            if callable(meth) and hasattr(meth, "url_rule_cache"):
                for url_postfix, http_methods, name in meth.url_rule_cache:

                    # ok, this is kind of weird.
                    # what we want to do is create a proxy view function from our method that flask can call like a
                    # regular view function. The straightforward way for that would just be to do:
                    #
                    # @functools.wraps(meth)
                    # def proxy(*args, **kwargs):
                    #   return meth(*args, **kwargs)
                    #
                    # and then pass proxy to add_url_rule.
                    #
                    # Because of the way closures in python work (they're not lexical, like in lisp or haskell),
                    # however, when a variable in a closure is reused in a loop (like meth and others are here),
                    # the closure will just point to the last version of that variable when the proxy function is
                    # finally called. We can fix this by adding a wrapper which takes meth as it's argument so
                    # each version of meth has it's own stack frame.
                    # see https://eev.ee/blog/2011/04/24/gotcha-python-scoping-closures/ for a
                    # good writeup.
                    # (Flask doesn't like partial (something to do with __name__), apparently,
                    # which is why we don't use it here.)

                    def wrapper(f):

                        # instantiate a new sleepyview object. note that this means that a separate endpoint instance is
                        # used for each custom routes, which shouldn't really be a problem unless the endpoint is
                        # stateful, which it really shouldnt be. Flask itself does this too: it constructs a new view
                        # for each call, even.

                        i = view_cls(session=session, **kwargs)
                        view = getattr(i, meth.__name__)

                        @functools.wraps(f)
                        def proxy_meth(*meth_args, **meth_kwargs):
                            response = view(*meth_args, **meth_kwargs)
                            return response

                        return proxy_meth

                    proxy = wrapper(meth)
                    proxy.__name__ = "{}_{}".format(view_name, name if name else meth.__name__)

                    try:
                        self.app.add_url_rule('%s%s' % (url_prefix, url_postfix),
                                              view_func=proxy,
                                              methods=http_methods)
                    except AssertionError as err:
                        raise Exception("Flask doesn't like this url rule. Did you put two route decorators"
                                        " on the same method and not give them explicit and distinct names?") from err


def route(url_postfix, methods=("GET", ), name=None):
    """
    Decorator for custom routes on sleepyviews.

    :param url_postfix: What is appended to the url prefix of the view the decorated method is defined on.
    :param methods: Allowed http methods on this url.
    """
    methods = tuple(methods)  # we need something hashable for the cache, which is a set.

    def decorator(f):
        if not hasattr(f, "url_rule_cache"):
            setattr(f, "url_rule_cache", set())

        f.url_rule_cache.add((url_postfix, methods, name))

        return f

    return decorator


class BaseSleepyView(MethodView):
    """
    The base class for constructing your own sleepy routed views. If you just want to use Marshmallow and SQLAlchemy,
    use SleepyView.
    """
    fields = []
    url_prefix = None
    name_prefix = None
    model = None
    db_adapter = None
    serializer = None

    def __init__(self, db_adapter=None, serializer=None, fields=None, **kwargs):

        """
        Initialize the sleepy view. This should not be called by the user itself. Flask calls this when it needs it.
        :param db_adapter: The adapter for the database. See :class:`~adapter.ModelAdapter`.
        :param serializer: The serializer. See :class:`~adapter.ModelSerializer`.
        :param fields: Fields used to change the object in te default update method(s).
        :param content_type: Content-Type put in the header of each response. If the serializer defines it's own, that
        one is used.
        """
        self.db_adapter = db_adapter
        self.serializer = serializer
        if fields:
            self.fields = fields


    def dispatch_request(self, *args, **kwargs):
        #
        response = super().dispatch_request(*args, **kwargs)

        content_type = getattr(self.serializer, "content_type", "application/json")

        # a method might return a response object or it might return (data, status, headers).
        if isinstance(response, tuple):
            headers = response[2] if len(response) == 3 else {}
            headers["Content-Type"] = content_type
            response = Response(response=response[0], status=response[1], headers=headers)

        elif isinstance(response, Response):
            response.headers["Content-Type"] = content_type
        else:
            raise Exception("Response was neither of type Response or tuple. Headers could not be set.")

        return response


    # We route to these methods, but all they do is delegate to the raw methods. (see below)

    def get(self, obj_id=None):
        """
        View to which GET /<url_prefix>/ and GET /<url_prefix>/<id>/ are routed.
        :param obj_id: The id of the object to get. If None, self.get_index is called, otherwise, self.get_entity(obj_id)
        is called.
        """
        if obj_id is not None:  # if we just go 'if obj_id' here, the router
            # gets confused when the obj_id is 0
            return self.get_entity(obj_id)
        else:
            return self.get_index()

    def post(self):
        """
        View to which POST /<url_prefix>/ is routed.
        """
        return self.post_index()

    def put(self, obj_id):
        """
        View to which PUT /<url_prefix>/<obj_id>/ is routed.
        """
        return self.put_entity(obj_id)

    def delete(self, obj_id):
        """
        View to which DELETE /<url_prefix>/ is routed.
        """
        return self.delete_entity(obj_id)


    # These methods take care of passing the data from the request to the correct raw methods and
    # build the response object:

    def get_index(self):
        """
        Method called when GET /<url_prefix>/ is called. Defaults to getting the representations of all objects using
        the self.get_all_raw method.
        """
        resp = Response(response=self.get_all_raw(),
                        status=200)

        return resp

    def post_index(self):
        """
        Method called when POST /<url_prefix>/ is called. Defaults to creating an object from the data passed
        in the body using the self.add_raw method.
        """
        json_repr = request.get_json()
        return self.add_raw(json_repr)

    def get_entity(self, obj_id):
        """
        Method called when GET /<url_prefix>/<obj_id> is called. Defaults to getting the object representation using the
        self.detail_raw method.
        """
        resp = Response(response=self.detail_raw(obj_id),
                        status=200)
        return resp

    def put_entity(self, obj_id):
        """
        Method called when PUT /<url_prefix>/<obj_id>/ is called. Defaults to updating the object to the one represented
        by the data passed in the body using the self.edit_raw method
        """
        json_repr = request.get_json()

        resp = Response(response=self.edit_raw(obj_id, json_repr),
                        status=200)
        return resp

    def delete_entity(self, obj_id):
        """
        Method called when DELETE /<url_prefix>/ is called. Defaults to calling self.destroy() (because it doesn't take
        or return any data by default, we skip the raw method here)
        """
        return self.destroy(obj_id)


    # These 'raw' methods take care of the (un)marshalling of the objects going into and coming out of the 'action'
    # methods:


    def get_all_raw(self):
        """
        Marshall the output of self.list() using the serializer.
        """
        return self.serializer.marshall_objs(self.list())

    def detail_raw(self, obj_id):
        """
        Marshall the output of self.detail(obj_id) using the serializer.
        """
        return self.serializer.marshall_obj(self.detail(obj_id))


    def add_raw(self, json_repr):
        """
        Marshall the input to and output of self.create(obj_id) using the serializer.
        """
        try:
            obj = self.serializer.unmarshall_obj(json_repr)
            return self.create(obj)
        except SerializationException as e:
            resp = Response(response=e.json,
                            status=400)
            return resp


    def edit_raw(self, obj_id, json_repr):
        """
        Marshall the input to and output of self.edit(obj_id) using the serializer.
        """
        try:
            obj = self.serializer.unmarshall_obj(json_repr)
            return self.serializer.marshall_obj(self.edit(obj_id, obj))
        except SerializationException as e:
            resp = Response(response=e.json,
                            status=400)
            return resp


    # These CRUDL methods define the actual operation.

    def list(self):
        """
        Return a list of all objects.
        """
        return self.db_adapter.get_all()

    def create(self, obj):
        """
        Create an object.
        """
        self.db_adapter.add_obj(obj)
        return "", 204

    def detail(self, obj_id):
        """
        Return the object with the provided obj_id.
        """
        return self.db_adapter.get_obj(obj_id)

    def edit(self, obj_id, updated_obj):
        """
        Update the object with the provided obj_id to be the updated_obj.
        """
        return self.db_adapter.update_obj(obj_id, updated_obj)

    def destroy(self, obj_id):
        """
        Delete the object with the provided obj_id.
        """
        self.db_adapter.delete_obj(obj_id)
        return "", 200


class SleepyView(BaseSleepyView):
    """
    View class using a Marshmallow schema and a Flask-SQLAlchemy model to do most, if not all of the work for you.

    Example usage:

    app = Flask(__name__)
    db = SQLAlchemy(app)
    ma = Marshmallow(app)

    sleepy = Sleepy(app, db)

    class Widget(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)

    class WidgetSchema(ma.Schema)
        id = ma.Int()
        name = ma.Str()


    class WidgetSleepyView(SleepyView):
        model = Widget # SQLAlchemy model
        schema = WidgetSchema
        fields = ["name"]

    sleepy.register(WidgetSleepyView, url_prefix="/widget", name_prefix="widget")

    You are now able to:
    - get a list of all widgets using GET /widget/
    - get the widget with id <obj_id> using GET /widget/<obj_id>/
    - create a widget using POST /widget/
    - update the widget with id <obj_id> PUT /widget/<obj_id>/
    - delete the widget with id <obj_id> DELETE /widget/<obj_id>/

    This behaviour can be modified by overriding the methods defined in BaseSleepyView. There are three layers of methods:
    - routing: the methods the flask routing is pointed to. These call the data methods.
    - data: the methods passing raw data to the raw methods and creating responses from what they return
    - raw: the methods doing the serialization and passing input and output to and from the CRUDL methods
    - CRUDL: the methods defining the actual actions being performed.

    Although there are enough use cases for overriding a method in one the first three layers, a lot of things can be
    done by only overriding the CRUDL-methods:

    class WidgetSleepyView(SleepyView):
        model = Widget # SQLAlchemy model
        schema = WidgetSchema # Marshmallow schema
        fields = ["name"]

        def create(self, obj):
            resp = super().create(obj)
            print("widget with name %s added to the database!" % obj.name)
            return resp


    You can also define custom routes postfixes on the view and even define multiple routes to the same method,
    provided you specify a name on at least all but one of them to allow Flask to differentiate between url rules.

     class WidgetSleepyView(SleepyView):
        model = Widget
        schema = WidgetSchema
        fields = ["name"]

        @route("/first/")
        def first(self):
            return super().detail(1)

        @route("/random/")
        @route("/arbitrary/", name="arbitrary")
        def random(self):
            return random.choice(super().list(obj))

    Adding custom routes to methods routed by sleepy itself isn't possible yet.

    """
    model = None
    schema = None
    fields = []

    def __init__(self, session, **kwargs):

        fields = kwargs.pop("fields", self.fields)
        schema = kwargs.pop("schema", self.schema)
        model = kwargs.pop("model", self.model)

        db_adapter = SQLAModelAdapter(model=model, session=session, fields=fields)
        serializer = MarshmallowSchemaSerializer(schema)
        super().__init__(db_adapter=db_adapter, serializer=serializer, **kwargs)
