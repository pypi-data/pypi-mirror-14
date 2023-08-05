from flask import json, abort
from flask.ext.marshmallow.fields import URLFor, Hyperlinks
from marshmallow_sqlalchemy import ModelSchema


class AbstractDataModelMixin(object):

    def count(self):
        raise NotImplementedError()

    def get_all(self):
        raise NotImplementedError()

    def add_obj(self, obj):
        raise NotImplementedError()

    def get_obj(self, obj_id):
        raise NotImplementedError()

    def delete_obj(self, obj_id):
        raise NotImplementedError()

    def update_obj(self, obj_id, updated_obj):
        raise NotImplementedError()

    # def determine_fields_from_model(self, model):
    #     raise NotImplementedError()


class AbstractSerializationMixin(object):

    def unmarshall_obj(self, json_repr):
        raise NotImplemented()

    def marshall_obj(self, obj):
        raise NotImplemented()

    def marshall_objs(self, objs):
        return json.dumps([self.marshall_obj(obj) for obj in objs])


class SQLAModelMixin(AbstractDataModelMixin):
    session = None
    model = None
    fields = None

    def get_all(self):
        return self.model.query.all()

    def add_obj(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get_obj(self, obj_id):
        obj = self.model.query.get(obj_id)
        if not obj:
            abort(404)
        return obj

    def update_obj(self, obj_id, updated_obj):
        obj = self.model.query.get(obj_id)

        for f in self.fields:
            setattr(obj, f, getattr(updated_obj, f))

        self.session.commit()
        return obj


    def delete_obj(self, obj_id):
        obj = self.get_obj(obj_id)
        self.session.delete(obj)
        self.session.commit()

    def count(self):
        return self.model.query.count()


class SerializationException(Exception):

    @property
    def json(self):
        return json.dumps({"message": "your input could not be serialized"})

    pass


class MarshmallowException(SerializationException):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors

    @property
    def json(self):
        return json.dumps({"message": "your input could not be serialized",
                           "errors": self.errors})





class MarshmallowSchemaMixin(AbstractSerializationMixin):

    def unmarshall_obj(self, json_repr):
        if not json_repr:
            raise SerializationException()

        data, errors = self.schema().load(json_repr)
        if errors:
            raise MarshmallowException(errors)
        return data

    def marshall_obj(self, obj):
        return bytes(self.schema(many=False).dumps(obj).data, encoding="utf-8")

    def marshall_objs(self, objs):
        return bytes(self.schema(many=True).dumps(objs).data, encoding="utf-8")
