from flask import Response, request
from flask.views import MethodView
from sleepy.adapter import MarshmallowSchemaMixin, SQLAModelMixin, AbstractSerializationMixin, AbstractDataModelMixin, \
    SerializationException

__author__ = 'robin'


class BaseSleepyView(MethodView, AbstractSerializationMixin, AbstractDataModelMixin):
    """
    The base class for constructing your own sleepy routed views. If you just want to use Marshmallow and SQLAlchemy,
    use SleepyView.
    """
    fields = []
    url_prefix = None
    name_prefix = None
    model = None
    content_type = "application/json"

    def __init__(self):
        pass

    def dispatch_request(self, *args, **kwargs):

        response = super().dispatch_request(*args, **kwargs)


        # a method might return a response object or it might return (data, status, headers).
        if isinstance(response, tuple):
            headers = response[2] if len(response) == 3 else {}
            headers["Content-Type"] = self.content_type
            response = Response(response=response[0], status=response[1], headers=headers)

        elif isinstance(response, Response):
            response.headers["Content-Type"] = self.content_type
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
        return self.marshall_objs(self.list())

    def detail_raw(self, obj_id):
        """
        Marshall the output of self.detail(obj_id) using the serializer.
        """
        return self.marshall_obj(self.detail(obj_id))


    def add_raw(self, json_repr):
        """
        Marshall the input to and output of self.create(obj_id) using the serializer.
        """
        try:
            obj = self.unmarshall_obj(json_repr)
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
            obj = self.unmarshall_obj(json_repr)
            return self.marshall_obj(self.edit(obj_id, obj))
        except SerializationException as e:
            resp = Response(response=e.json,
                            status=400)
            return resp


    # These CRUDL methods define the actual operation.

    def list(self):
        """
        Return a list of all objects.
        """
        return self.get_all()

    def create(self, obj):
        """
        Create an object.
        """
        self.add_obj(obj)
        return "", 204

    def detail(self, obj_id):
        """
        Return the object with the provided obj_id.
        """
        return self.get_obj(obj_id)

    def edit(self, obj_id, updated_obj):
        """
        Update the object with the provided obj_id to be the updated_obj.
        """
        return self.update_obj(obj_id, updated_obj)

    def destroy(self, obj_id):
        """
        Delete the object with the provided obj_id.
        """
        self.delete_obj(obj_id)
        return "", 204


class SleepyView(BaseSleepyView, MarshmallowSchemaMixin, SQLAModelMixin):
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

    This behaviour can be modified by overriding the methods defined in BaseSleepyView.
    There are three layers of methods:
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

    pass