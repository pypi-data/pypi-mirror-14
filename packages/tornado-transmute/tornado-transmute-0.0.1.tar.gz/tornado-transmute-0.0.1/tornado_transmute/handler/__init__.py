import tornado.web
from web_transmute import default_context
from .parameters import get_param_extractor


class HandlerFactory(object):
    """
    HandleFactory handles aggregating transmute functions
    into a set of handlers.
    """

    def __init__(self):
        self._handlers = {}

    def add_handler(self, path, transmute_func):
        if path not in self._handlers:
            self._handlers[path] = _create_handler()

        handler = self._handlers[path]

        _add_transmute_func_to_handler(transmute_func, handler)

    def get_handler_tuples(self):
        handlers = []
        for path, handler in self._handlers.items():
            handlers.append((path, handler))
        return handlers


def _create_handler():

    class Handler(tornado.web.RequestHandler):
        pass

    return Handler


def _add_transmute_func_to_handler(transmute_func, handler,
                                   context=default_context):
    handler_method = generate_handler_method(transmute_func)

    is_get = True

    for method in transmute_func.http_methods:
        is_get = False
        setattr(handler, method.lower(), handler_method)

    if is_get:
        setattr(handler, "get", handler_method)


def generate_handler_method(transmute_func, context=default_context):

    extract_args = get_param_extractor(transmute_func, context)

    def method(self, *args):
        try:
            args, kwargs = extract_args(self, args=args)
            result = transmute_func.raw_func(self, *args, **kwargs)
            self.set_header("Content-Type", "application/json")
            self.write({
                "success": True,
                "result": result
            })
        except Exception as e:
            if (transmute_func.error_exceptions and
               isinstance(e, transmute_func.error_exceptions)):
                self.write({
                    "success": False,
                    "details": str(e)
                })
            else:
                raise
    method.transmute_func = transmute_func

    return method
