import os

import tornado.testing

from aprp import settings
from aprp.aprp import make_app, options
app = make_app()

class TestHandlerBase(tornado.testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestHandlerBase, self).setUp()

    def _make_headers(self, _range):
        return {'Range': _range}

    def get_app(self):
        return app

    def _get_url(self, path):
        return 'http://localhost:{}/{}'.format(
            self.get_http_port(),
            path)

class TestAsyncPyRangeProxyHandler(TestHandlerBase):

    def test_request_without_filename(self):
        def _callback(response):
            self.assertEqual(response.code, 404)
            self.stop()

        client = tornado.testing.AsyncHTTPClient(self.io_loop)
        client.fetch(self._get_url(''), _callback)
        self.wait()

    def test_request_without_range_header(self):
        def _callback(response):
            self.assertEqual(response.code, 503)
            self.stop()

        client = tornado.testing.AsyncHTTPClient(self.io_loop)
        client.fetch(self._get_url('myfilename'), _callback)
        self.wait()

    def test_request_with_range_support_check(self):
        def _callback(response):
            self.assertEqual(response.code, 200)
            self.stop()

        client = tornado.testing.AsyncHTTPClient(self.io_loop)
        client.fetch(self._get_url('myfilename'),
            _callback,
            headers=self._make_headers(''))
        self.wait()
