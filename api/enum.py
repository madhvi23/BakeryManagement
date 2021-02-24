from enum import Enum


class HttpConstants(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'


class ResponseConstants(Enum):
    SUCCESS = 'success'
    FAIL = 'Fail'


class OrderStatus(Enum):
    PLACED = 'Placed'
    DELIVERED = 'Delivered'
    INPROCESS = "In Process"
    DISPATCH = "Dispatched"