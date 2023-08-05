import os

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line
from tornadoredis import Client

from backend.handlers import (
    TrainerHandler, ClassifierHandler, InterfaceHandler,
    StatsHandler, LabelsHandler, StatsWSHandler,
    WordsHandler
)


class Klassify(Application):
    debug = True

    def __init__(self, command_options):
        self.options = command_options

        handlers = self.get_handlers()

        super(Klassify, self).__init__(
            handlers,
            debug=self.debug
        )

        self.redis = Client(
            options.redis_host,
            options.redis_port,
            selected_db=options.redis_db
        )

    def get_handlers(self):
        return [
            (r'/train', TrainerHandler),
            (r'/classify', ClassifierHandler),
            (r'/stats', StatsHandler),
            (r'/words/(?P<label>[\w-]+)', WordsHandler),
            (r'/labels', LabelsHandler),
            (r'/', InterfaceHandler),
            (r'/ws', StatsWSHandler),

            (r'/dist/(.*)', StaticFileHandler, {
                'path': os.path.join(os.path.dirname(__file__), "dist")
            })
        ]


define("port", default=8888, help="run on the given port", type=int)
define('redis_port', default=6379, help="redis port", type=int)
define('redis_host', default='localhost', help="redis host", type=str)
define('redis_db', default=0, help="redis database", type=int)
define('prefix', default='klassify',
       help="prefix that will be used in redis keys", type=str)


def main():
    parse_command_line()
    http_server = HTTPServer(Klassify(options))
    http_server.listen(options.port)

    print('Klassify is running on localhost:%s' % options.port)

    IOLoop.instance().start()


if __name__ == '__main__':
    main()
