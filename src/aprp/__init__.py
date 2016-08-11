import tornado.ioloop
import tornado.web

class AsyncPyRangeProxyHandler(tornado.web.RequestHandler):

    
    def _prep_headers(self):
        _bytes = 'bytes'
        if self._is_range():
            pass
        self.set_header('Accept-Ranges', _bytes)


    def _handle_request(self, filename, start, end):
        pass

    def head(self):
        self.write("Hello, world")    


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
        self.finish()


class RangeParamHandler(AsyncPyRangeProxyHandler):

    @tornado.web.asynchronous
    def get(self, filename, start, end=None):
        self._handle_request(filename, start, end)
        self.finish()

