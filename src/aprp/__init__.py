import tornado.ioloop
import tornado.web
import tornado.httpclient

from . import settings

class AsyncPyRangeProxyHandler(tornado.web.RequestHandler):

    def _prep_response_headers(self, response):
        _bytes , content_length = 'bytes', ''
        self.set_header('Accept-Ranges', _bytes)
        try:
            content_length = response.headers['Content-Length']
            length = content_length.split('/')[1]
            length = int(length)
        except KeyError as ke:
            raise ke
            pass
        except IndexError as ie:
            content_length = response.headers['Content-Length']
            pass
        except ValueError as ve:
            raise ve
            pass

        finally:
            self.set_header('Content-Length', content_length)

    def _make_url(self, filename):
        return '{}/{}'.format(settings.UPSTREAM, filename)

    def _make_upstream_request(self, filename, start, end):

        return tornado.httpclient.HTTPRequest(
            self._make_url(filename),
            method='GET',
            headers=self._prep_upstream_headers(start, end)
        )

    def _prep_upstream_headers(self, start=None, end=None):
        if not start:
            _range = ''
        else:
            if not end:
                end = ''

        _range = 'bytes={}-{}'.format(start, end)

        return dict(Range=_range)

    def _call_upstream_blocking(self, filename, start, end):

        http_client = tornado.httpclient.HTTPClient()

        try:
            request = self._make_upstream_request(filename, start, end)
            return http_client.fetch(request)
        except tornado.httpclient.HTTPError as e:
            raise e
            pass
        except Exception as e:
            raise e
            pass

    def _call_upstream_non_blocking(self, filename, start, end):
        def handle_response(response):
            if not response.error:
                self._prep_response_headers(response)

                self.write(response.body)
                self.finish()
            else:
                pass
        
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(self._make_url(filename), handle_response)


    def _handle_request(self, filename, start, end):
        # NICE-TO-HAVE add internal caching
        # and serve from cache when possible
        if not start:
            # we have a support range request?
            # let's get the conent length
            response = self._call_upstream_blocking(filename, 0, None)
            self._prep_response_headers(response)
            self.write(response.body)
            self.finish()

        self._call_upstream_non_blocking(filename, start, end)

class RangeHeaderHandler(AsyncPyRangeProxyHandler):

    def _is_range(self):
        val = self.request.headers.get('Range', None)
        if bool(val) and '=' in val:
            return True
        return False

    def _parse_range(self, val):
        try:
            _range = val.split('=')[1].split('-')
        except IndexError as ie:
            #TO-DO handle with this
            pass

        return _range[0], _range[1]


    def _get_range(self):
        if not self._is_range():
            if not 'Range' in self.request.headers:
                # we do not support full media requests                
                raise tornado.web.HTTPError(503)

            return None, None

        val = self.request.headers.get('Range', None)
        return self._parse_range(val)
    
    @tornado.web.asynchronous
    def get(self, filename):
        start, end = self._get_range()
        self._handle_request(filename, start, end)

class RangeParamHandler(AsyncPyRangeProxyHandler):

    @tornado.web.asynchronous
    def get(self, filename, start, end=None):
        self._handle_request(filename, start, end)
