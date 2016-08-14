import tornado.ioloop
import tornado.web
import tornado.httpclient

from . import settings
from .settings import logger

class AsyncPyRangeProxyHandler(tornado.web.RequestHandler):
    """
        Abstract class for handling requests.
        There are two types of range requests supported:
        1. Range in request headers
        2. Range as URL param, as in : 
            - /myfilename/<start>/<end>
            - /myfilename.mp4/1234/789
    """

    def _is_range(self):
        """
            Checking to make sure the client
            is sending a range request.
        """
        val = self.request.headers.get('Range', None)
        if bool(val) and '=' in val:
            return True
        return False

    def _parse_range(self, val):
        """
            Parsing the values in the Range header.
        """
        try:
            _range = val.split('=')[1].split('-')
        except IndexError as ie:
            #TO-DO handle with this
            pass

        return _range[0], _range[1]


    def _get_range(self):
        """
            Returns the start and end
            position of the request media.
            Start and end are extracted from
            the Range header.
        """
        if not self._is_range():
            if not 'Range' in self.request.headers:
                # we do not support full media requests                
                raise tornado.web.HTTPError(503)

            return None, None

        val = self.request.headers.get('Range', None)
        return self._parse_range(val)

    def _prep_response_headers(self, response):
        """
            Examining and returning content-length
            from upstream.
        """
        _bytes , content_length = 'bytes', ''
        self.set_header('Accept-Ranges', _bytes)
        self.set_header('Content-Length', response.headers.get('Content-Length', '0'))
            

    def _make_url(self, filename):
        """
            Abstract UPSTREAM to settings for better
            portability.
        """
        return '{}/{}'.format(settings.UPSTREAM, filename)

    def _make_upstream_request(self, filename, start, end):
        """
            Call upstream server
        """
        return tornado.httpclient.HTTPRequest(
            self._make_url(filename),
            method='GET',
            headers=self._prep_upstream_headers(start, end)
        )

    def _prep_upstream_headers(self, start=None, end=None):
        """
            Prepping upstream headers.
            If start is None then we are getting content length 
        """
        if not start:
            _range = ''
        else:
            if not end:
                end = ''

        _range = 'bytes={}-{}'.format(start, end)

        return dict(Range=_range)

    def _call_upstream_blocking(self, filename, start, end):
        """
            Synchronous call to upstream server.
            Used for getting content length upon
            the client sending a support range check.
        """
        http_client = tornado.httpclient.HTTPClient()

        try:
            logger.info("reverse proxying media {}".format(filename))
            logger.info("getting {} to {}".format(start, end))
            request = self._make_upstream_request(filename, start, end)
            return http_client.fetch(request)
        except tornado.httpclient.HTTPError as e:
            logger.error("http error :")
            logger.error(e)
            raise tornado.web.HTTPError(500)
        except Exception as e:
            logger.error(e)
            raise tornado.web.HTTPError(500)

    def _call_upstream_non_blocking(self, filename, start, end):
        """
            Async call to upstream. This is where the proxying
            is done.
        """
        logger.info("calling upstream to get content length of media {}".format(filename))
        def handle_response(response):
            if not response.error:
                self._prep_response_headers(response)

                self.write(response.body)
                self.finish()
            else:
                logger.error("calling upstream failed")
                logger.error(response.errors)
                raise tornado.web.HTTPError(500)
        
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(self._make_url(filename), handle_response)


    def _handle_request(self, filename, start, end):
        """
            Abstract function to kick of the proxying.
            First we check to see if its a support range
            request, then return the content lenght
            from upstream.
            Else we reverse proxy to upstream.

        """
        logger.info("handling get for media: {}".format(filename))
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
    """
        Support for range in header.
    """
    
    @tornado.web.asynchronous
    def get(self, filename):
        """
            GET request handler.
        """
        start, end = self._get_range()
        self._handle_request(filename, start, end)

class RangeParamHandler(AsyncPyRangeProxyHandler):

    @tornado.web.asynchronous
    def get(self, filename, start, end=None):
        """
            GET request handler.
        """
        #get the range in headers
        header_start, header_end = self._get_range()
        if header_start or header_end:
            if header_start != start or \
                header_end != end:
                #range is request in headers
                #and in params as diff values
                raise tornado.web.HTTPError(416)
        self._handle_request(filename, start, end)
