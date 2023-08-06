import tornado.testing
import tornado.web
import tornado_transmute
import json


def _create_app():
    app = tornado.web.Application([
        ("/foo/([^\/]+)", ExampleHandler)
    ])
    swagger_handler = tornado_transmute.generate_swagger_json_handler(app)
    tornado_transmute.add_swagger_static_routes(
        app, "/swagger", "/swagger.json"
    )
    app.add_handlers(".*", [("/swagger.json", swagger_handler)])
    return app


class TestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return _create_app()

    def test_foo(self):
        resp = self.fetch("/foo/bar")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json.get("success")
        assert resp_json.get("result") == 2

    def test_foo_queryparam(self):
        resp = self.fetch("/foo/bar?multiplier=2")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json.get("success")
        assert resp_json.get("result") == 4

    def test_swagger_json(self):
        resp = self.fetch("/swagger.json")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert "get" in resp_json["paths"]["/foo/([^\/]+)$"]
        assert resp_json["swagger"] == "2.0"
        assert resp_json["info"] == {
            "title": "swagger", "version": "1.0"
        }

    def test_swagger_body(self):
        resp = self.fetch("/swagger")
        assert resp.code == 200
        body = resp.body.decode("UTF-8")
        assert "swagger-section" in body


class ExampleHandler(tornado.web.RequestHandler):

    @tornado_transmute.to_route()
    @tornado_transmute.annotate({
        "resource": str, "multiplier": int,
        "return": int
    })
    def get(self, resource, multiplier=1):
        return 2 * multiplier

if __name__ == "__main__":
    app = _create_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
