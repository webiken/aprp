import os

from tornado.testing import AsyncHTTPTestCase

from aprp.aprp import make_app, options

class TestHandlerBase(AsyncHTTPTestCase):

    def setUp(self):
        super(TestHandlerBase, self).setUp()

    def get_app(self):
        return make_app()

class TestAsyncPyRangeProxyHandler(TestHandlerBase):

    def test_root_url(self):

        response = self.fetch('/', method='HEAD')
        self.assertEqual(response.code, 200)
