import tornado.ioloop
import tornado.web
from tornado.websocket import WebSocketHandler
import sys, getopt
import tornadoredis
import tornado.gen
import settings

verbose = False
authorization_backend = None
redis_client = tornadoredis.Client()
redis_client.connect()


def debug(msg):
    if verbose:
        print(msg)


def get_params_from_uri(uri):
    uri = uri.split('?')
    assert len(uri) <= 2, 'Passed URI was formatted incorrectly. Multiple ? signs.'
    uri = uri[1] if len(uri) > 1 else uri[0]
    raw_params = uri.split('&')
    params = {}
    for param in raw_params:
        param = param.split('=')
        if len(param) == 2:
            params[param[0]] = param[1]
    return params


class MessageHandler(WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)
        debug("MessageHandler created")
        params = get_params_from_uri(args[1].uri)
        self.client = None
        self.channels = None
        self.authorization_backend = authorization_backend if authorization_backend is not None else None
        self.listen(**params)

    @tornado.gen.coroutine
    def listen(self, **kwargs):
        if self.authorize():
            self.client = tornadoredis.Client()
            self.client.connect()
            if 'sub' in kwargs:
                self.channels = kwargs['sub'].split(',')
                yield tornado.gen.Task(self.client.subscribe, self.channels)
            self.client.listen(self.on_message)

    def open(self):
        self.write_message('hello')
        debug("On open")

    def on_message(self, message):
        debug("Got message: " + str(message))
        if isinstance(message, tornadoredis.client.Message):
            self.write_message(str(message.body))
        else:
            self.write_message(str(message.body))

    def on_close(self):
        debug("On close")
        for channel in self.channels:
            self.client.unsubscribe(channel)
            self.client.disconnect()

    def check_origin(self, origin):
        debug("Check origin: " + origin)
        return True

    def authorize(self):
        if self.authorization_backend is not None:
            if isinstance(self.authorization_backend, str):
                self.init_auth_backend()
            return self.authorization_backend.authorize(self)
        return True

    def init_auth_backend(self):
        parts = self.authorization_backend.split('.')
        module = __import__('.'.join(parts[0:-1]))
        self.authorization_backend = getattr(module, parts[-1])()


def check_origin(self, origin):
    debug("Origin: " + origin)
    return True


class WebSocketServer:
    def __init__(self, settings=settings, auth=None):
        port = settings.WEBSOCKET_SERVER_PORT
        help_text = 'server.py -p <port>'
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hvp:", ["port="])
        except getopt.GetoptError:
            print(help_text)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print(help_text)
                sys.exit()
            elif opt == '-v':
                global verbose
                verbose = True
            elif opt in ("-p", "--port"):
                port = int(arg)

        app = self.make_app(auth=auth)
        app.listen(port)

        print("WebSocket server running on port {0}".format(port))
        tornado.ioloop.IOLoop.current().start()


    @staticmethod
    def make_app(auth=None):
        global authorization_backend
        authorization_backend = auth

        return tornado.web.Application([
            (r"/connect", MessageHandler)
        ])


if __name__ == "__main__":
    WebSocketServer()

