# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from bbz.handler.UserHandler import QueryUserHandler
from tornado.routing import (
    RuleRouter,
    Rule,
    AnyMatches,
    PathMatches
)
import threading
from tornado.options import (
    define,
    options
)

port = 8083
define("port", default=port, help="run on the given port", type=int)



class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        # self.db = torndb.Connection(
        #     host="{host}:{port}".format(
        #         host=fetch_args("db").get("host"),
        #         port=fetch_args("db").get("port")),
        #     database=fetch_args("db").get("database"),
        #     user=fetch_args("db").get("user"),
        #     password=str(fetch_args("db").get("password")))
        #
        # self.db = torndb.Connection("localhost:3306", "demo_new", "root", "123456")


def main():
    # tornado.options.parse_command_line()
    settings = {

    }

    application = Application([
        (r"/test/user", QueryUserHandler),
    ], **settings)

    router = RuleRouter(
        [
            Rule(AnyMatches(), application),
        ]
    )
    http_server = tornado.httpserver.HTTPServer(router)
    http_server.listen(options.port)
    t = threading.Thread()
    t.setDaemon(True)
    t.start()
    tornado.ioloop.IOLoop.instance().start()
    t.join()


if __name__ == "__main__":
    main()
