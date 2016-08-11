#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from settings import logger, PORT

define("port", default=PORT, help="run on the given port", type=int)

class AsyncPyRangeProxyHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write("Hello, world")

    head = get

def make_app():
    tornado.options.parse_command_line()
    return tornado.web.Application([
        (r'.*', AsyncPyRangeProxyHandler),
    ])

def start_proxy(app):
    logger.info("starting http server at port {}".format(PORT))
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

def main():

    app = make_app()
    start_proxy(app)

if __name__ == '__main__':
    main()