from flask import json

from sleepy.exceptions import SleepyException, SerializationException, MarshmallowException


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

    def get_obj(self, obj_id, abort_on_not_found=True):
        obj = self.model.query.get(obj_id)
        if not obj and abort_on_not_found:
            raise SleepyException(status_code=404,
                                  message="no object of type {} found with id {}".format(self.model, obj))
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


class MarshmallowSchemaMixin(AbstractSerializationMixin):

    def unmarshall_obj(self, json_repr, many=False):
        if not json_repr:
            raise SerializationException()

        data, errors = self.schema(many=many).load(json_repr)
        if errors:
            raise MarshmallowException(errors)
        return data

    def unmarshall_objs(self, json_repr):
        return self.unmarshall_obj(json_repr, many=True)

    def marshall_obj(self, obj):
        return bytes(self.schema(many=False).dumps(obj).data, encoding="utf-8")

    def marshall_objs(self, objs):
        return bytes(self.schema(many=True).dumps(objs).data, encoding="utf-8")
