from collections import defaultdict
from swagger_schema import Swagger, Info, Path
from web_transmute.swagger import (
    generate_swagger,
    get_swagger_static_root
)
import tornado.web

METHODS = ["get", "post", "delete", "put"]
STATIC_ROOT = "/_swagger/static"


def generate_swagger_json(app, title="swagger"):
    """
    from a tornado application, generate a swagger dict
    for all of the transmute routes available.
    """
    paths = defaultdict(Path)
    for domain, specs in app.handlers:
        for s in specs:
            path = s.regex.pattern
            handler = s.handler_class
            for m in METHODS:
                method = getattr(handler, m)
                if hasattr(method, "transmute_func"):
                    setattr(paths[path], m, method.transmute_func.swagger)
    return Swagger(
        info=Info(title=title, version="1.0"),
        paths=paths,
        swagger="2.0"
    ).dump()


def generate_swagger_json_handler(app, title="swagger"):

    swagger_json = generate_swagger_json(app, title=title)

    class SwaggerSpecHandler(tornado.web.RequestHandler):

        def get(self):
            self.write(swagger_json)
            self.finish()

    return SwaggerSpecHandler


def add_swagger_static_routes(app, target_route, swagger_json_route):
    static_root = get_swagger_static_root()
    swagger_body = generate_swagger(STATIC_ROOT, swagger_json_route)

    class SwaggerBodyHandler(tornado.web.RequestHandler):

        def get(self):
            self.write(swagger_body)
            self.finish()

    app.add_handlers(".*", [
        (target_route, SwaggerBodyHandler),
        (STATIC_ROOT + "/(.*)", tornado.web.StaticFileHandler, {"path": static_root})
    ])
