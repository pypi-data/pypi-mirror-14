from flask import jsonify, json


class SleepyException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ObjectNotInRelation(SleepyException):
    status_code = 400


class SerializationException(SleepyException):

    def __init__(self):
        super().__init__(status_code=400, message="your input could not be serialized")

class MissingBodyKey(SleepyException):
    def __init__(self, key):
        super().__init__(status_code=400, message="Missing key {} in body.".format(key))


class MarshmallowException(SerializationException):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors

    def to_dict(self):
        rv = super().to_dict()
        rv["errors"] = self.errors
        return rv