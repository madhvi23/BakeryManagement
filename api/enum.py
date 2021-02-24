from enum import Enum


class HttpConstants(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'


class ResponseConstants(Enum):
    SUCCESS = 'success'
    FAIL = 'Fail'
