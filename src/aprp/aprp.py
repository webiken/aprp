#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

import aprp
from aprp.settings import logger, PORT

define("port", default=PORT, help="run on the given port", type=int)

def make_app():
    tornado.options.parse_command_line()
    return tornado.web.Application([
        (r"/(?P<filename>[^\/]+)", aprp.RangeHeaderHandler),
        (r"/(?P<filename>[^\/]+)/(?P<start>[^\d]+)/(?P<end>[^\d]+)?", aprp.RangeParamHandler),
    ])

def start_proxy(app):
    logger.info("starting http server at port {}".format(PORT))
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

