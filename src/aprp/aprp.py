#!/usr/bin/env python

import tornado.ioloop
import tornado.web
from tornado.options import options, parse_command_line

from settings import logger, PORT

options.logging = None
parse_command_line()

class AsyncPyRangeProxyHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write("Hello, world")

def make_app():
    logger.info("creating web application with AsyncPyRangeProxyHandler")
    return tornado.web.Application([
        (r'.*', AsyncPyRangeProxyHandler),
    ])

def start_proxy():
    logger.info("starting async lisent on HTTP Server at port {}".format(PORT))
    tornado.ioloop.IOLoop.current().start()

def main():
    app = make_app()
    app.listen(PORT)

    start_proxy()

if __name__ == '__main__':
    logger.info("staring proxy")
    main()