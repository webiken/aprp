#!/usr/bin/env python

import tornado.httpserver
import tornado.web

import settings

class AsyncPyRangeProxyHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        pass

def main():
    """
    """
    app = tornado.web.Application([
        (r'.*', AsyncPyRangeProxyHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(settigns.PORT)

    tornado.ioloop.IOLoop.instance()

if __name__ == '__main__':
    main()