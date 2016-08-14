import os
from unittest.mock import MagicMock

import tornado.testing

from aprp import settings
from aprp.aprp import make_app, options
from aprp import tornado

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

    def _make_request(self, url):
        return tornado.httpclient.HTTPRequest(url, method='GET')

    def _mock_response(self, request):
        class Buffer(object):
            def getvalue(self):
                return "myfilename"

        response = tornado.httpclient.HTTPResponse(request,
            200,
            headers={'Content-Length' : '10'}, buffer=Buffer())
        
        return response


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

        request = self._make_request('http://localhost:9000/myfilename')
        future = self._mock_response(request)
        tornado.httpclient.HTTPClient.fetch = MagicMock(return_value=future)

        client = tornado.testing.AsyncHTTPClient(self.io_loop)
        client.fetch(self._get_url('myfilename'),
            _callback,
            headers=self._make_headers(''))
        self.wait()
