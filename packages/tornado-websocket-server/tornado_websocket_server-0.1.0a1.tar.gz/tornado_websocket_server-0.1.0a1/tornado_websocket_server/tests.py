from tornado import testing
from tornado.httpclient import HTTPRequest
from server import WebSocketServer
from tornado import testing, httpserver, gen, websocket
from helpers import push_event
from authorization import AbstractAuthorization


class WebSocketSimpleTest(testing.AsyncHTTPTestCase):

    def get_app(self):
        app = WebSocketServer.make_app()
        return app

    def test_404(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 404)

    def test_400(self):
        response = self.fetch('/connect')
        self.assertEqual(response.code, 400)


class WebSocketBetterTest(testing.AsyncTestCase):

    def setUp(self):
        super(WebSocketBetterTest, self).setUp()
        server = httpserver.HTTPServer(WebSocketServer.make_app())
        socket, self.port = testing.bind_unused_port()
        server.add_socket(socket)

    def _mk_connection(self):
        return websocket.websocket_connect(
            'ws://localhost:{}/connect?sub=test_channel'.format(self.port)
        )

    @gen.coroutine
    def _mk_client(self):
        c = yield self._mk_connection()
        _ = yield c.read_message()

        raise gen.Return(c)

    @testing.gen_test
    def test_hello(self):
        c = yield self._mk_connection()
        response = yield c.read_message()
        self.assertEqual('hello', response)

    @testing.gen_test
    def test_channels(self):
        c = yield self._mk_client()
        yield c.read_message()
        self.assertEqual(push_event("foo", ("test_channel",)), 1)
        response = yield c.read_message()
        self.assertEqual('"foo"', response)


class WebSocketDumbAuthTest(testing.AsyncTestCase):

    def setUp(self):
        super(WebSocketDumbAuthTest, self).setUp()
        server = httpserver.HTTPServer(WebSocketServer.make_app('authorization.Dumb'))
        socket, self.port = testing.bind_unused_port()
        server.add_socket(socket)

    def _mk_connection(self):
        return websocket.websocket_connect(
            'ws://localhost:{}/connect?sub=test_channel'.format(self.port)
        )

    @testing.gen_test
    def test_dumb(self):
        c = yield self._mk_connection()
        response = yield c.read_message()
        self.assertEqual('hello', response)


class WebSocketHeaderAuthTest(testing.AsyncTestCase):

    def setUp(self):
        class HeaderAuth(AbstractAuthorization):
            def authorize(self, handler):
                if 'Authorization' in handler.request.headers:
                    return handler.request.headers['Authorization'] == 'Test'
                return False

        super(WebSocketHeaderAuthTest, self).setUp()
        server = httpserver.HTTPServer(WebSocketServer.make_app(HeaderAuth()))
        socket, self.port = testing.bind_unused_port()
        server.add_socket(socket)

    def _mk_connection(self):
        request = HTTPRequest(
            'ws://localhost:{}/connect?sub=test_channel'.format(self.port),
            headers={
                'Authorization': 'Test'
            }
        )
        return websocket.websocket_connect(request)

    @testing.gen_test
    def test_authorized(self):
        c = yield self._mk_connection()
        response = yield c.read_message()
        self.assertEqual('hello', response)
