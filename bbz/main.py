# -*- coding: utf-8 -*-

import tornado
import torndb
import threading
import tornado.web

from bbz.handler.UserHandler import *
from bbz.utils.conf import (
    fetch_args
)
from tornado.routing import (
    RuleRouter,
    Rule,
    AnyMatches,
    PathMatches
)
from tornado.options import (
    define,
    options
)

'''应用端口'''
port = fetch_args("app").get("port")
define("port", default=port, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        self.db = torndb.Connection(
            host="{host}:{port}".format(
                host=fetch_args("db").get("host"),
                port=fetch_args("db").get("port")),
            database=fetch_args("db").get("database"),
            user=fetch_args("db").get("user"),
            password=str(fetch_args("db").get("password")))


def main():
    # tornado.options.parse_command_line()
    settings = {
        "debug": "debug"
    }
    '''路由配置url——处理类'''
    api = Application([
        (r"/test/user", QueryUserHandler),
        (r"/test/user/save", SaveUserHandler),
    ], **settings)

    router = RuleRouter(
        [
            Rule(AnyMatches(), api),
        ]
    )
    http_server = tornado.httpserver.HTTPServer(router)
    http_server.listen(options.port)

    t = threading.Thread()
    t.setDaemon(True)
    t.start()
    tornado.ioloop.IOLoop.instance().start()
    t.join()


if __name__ == '__main__':
    main()
