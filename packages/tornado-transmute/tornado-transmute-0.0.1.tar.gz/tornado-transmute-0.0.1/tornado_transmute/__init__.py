from web_transmute import *
from web_transmute.function import TransmuteFunction
from .handler import generate_handler_method
from .swagger import (
    generate_swagger_json,
    generate_swagger_json_handler,
    add_swagger_static_routes
)


def to_route(**options):

    def decorator(fn):
        transmute_func = TransmuteFunction(fn, **options)
        return generate_handler_method(transmute_func)

    return decorator
