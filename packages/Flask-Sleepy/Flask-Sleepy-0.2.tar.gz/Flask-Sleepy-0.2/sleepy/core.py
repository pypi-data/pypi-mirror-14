from sleepy.adapter import SQLAModelMixin
from sleepy.views import BaseSleepyView

from sleepy.routing import ListAttributeAccessor, RouteDecorated


class Sleepy(object):
    app = None
    db = None

    def __init__(self, app=None, db=None):

        """
        Initialize the Sleepy application. If you're using this directly you're not using
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

        SQLAModelMixin.session = session

        view_func = view_cls.as_view(name=view_name, **kwargs)

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
        names = []

        # find the methods decorated with routes and the attributes of type AttributeAccesor and loop through
        # their rule cache (see the route decorator below for an explantation)
        for attr_name in dir(view_cls):
            meth = getattr(view_cls, attr_name)
            if callable(meth):
                if isinstance(meth, RouteDecorated):  # this is a @route decorated method

                    meth.register(self.app, view_cls, url_prefix, **kwargs)

                elif isinstance(meth, ListAttributeAccessor):

                    meth.register(self.app, view_cls,
                                  url="{}<int:obj_id>/{}/".format(url_prefix, meth.attr_name),
                                  name="{}.{}".format(view_name, meth.attr_name),
                                  **kwargs)

                else:
                    pass
