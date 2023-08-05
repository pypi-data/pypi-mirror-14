"""HTTP Client library"""
import json


try:
    # Python 3
    import urllib.request as urllib
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    import urllib2 as urllib
    from urllib import urlencode


class Response(object):
    """Holds the response from an API call."""
    def __init__(self, response):
        """
        :param response: The return value from a open call
                         on a urllib.build_opener()
        :type response:  urllib response object
        """
        self._status_code = response.getcode()
        self._response_body = response.read()
        self._response_headers = response.info()

    @property
    def status_code(self):
        """
        :return: integer, status code of API call
        """
        return self._status_code

    @property
    def response_body(self):
        """
        :return: response from the API
        """
        return self._response_body

    @property
    def response_headers(self):
        """
        :return: dict of response headers
        """
        return self._response_headers


class Client(object):
    """Quickly and easily access any REST or REST-like API."""
    def __init__(self,
                 host,
                 request_headers=None,
                 version=None,
                 url_path=None):
        """
        :param host: Base URL for the api. (e.g. https://api.sendgrid.com)
        :type host:  string
        :param request_headers: A dictionary of the headers you want
                                applied on all calls
        :type request_headers: dictionary
        :param version: The version number of the API.
                        Subclass _build_versioned_url for custom behavior.
                        Or just pass the version as part of the URL
                        (e.g. client._("/v3"))
        :type version: integer
        :param url_path: A list of the url path segments
        :type url_path: list of strings
        """
        self.host = host
        self.request_headers = request_headers or {}
        self._version = version
        # _url_path keeps track of the dynamically built url
        self._url_path = url_path or []
        # These are the supported HTTP verbs
        self.methods = ['delete', 'get', 'patch', 'post', 'put']

    def _build_versioned_url(self, url):
        """Subclass this function for your own needs.
           Or just pass the version as part of the URL
           (e.g. client._('/v3'))
        :param url: URI portion of the full URL being requested
        :type url: string
        :return: string
        """
        return '{0}/v{1}{2}'.format(self.host, str(self._version), url)

    def _build_url(self, query_params):
        """Build the final URL to be passed to urllib

        :param query_params: A dictionary of all the query parameters
        :type query_params: dictionary
        :return: string
        """
        url = ''
        count = 0
        while count < len(self._url_path):
            url += '/{0}'.format(self._url_path[count])
            count += 1
        if query_params:
            url_values = urlencode(sorted(query_params.items()))
            url = '{0}?{1}'.format(url, url_values)
        url = self._build_versioned_url(url) if self._version else self.host + url
        return url

    def _update_headers(self, request_headers):
        """Update the headers for the request

        :param request_headers: headers to set for the API call
        :type response: dictionary
        :return: dictionary
        """
        self.request_headers.update(request_headers)

    def _build_client(self, name=None):
        """Make a new Client object

        :param name: Name of the url segment
        :type name: string
        :return: A Client object
        """
        url_path = self._url_path+[name] if name else self._url_path
        return Client(host=self.host,
                      version=self._version,
                      request_headers=self.request_headers,
                      url_path=url_path)

    def _make_request(self, opener, request):
        """Make the API call and return the response. This is separated into
           it's own function, so we can mock it easily for testing.

        :param opener:
        :type opener:
        :param request: url payload to request
        :type request: urllib.Request object
        :return: urllib response
        """
        return opener.open(request)

    def _(self, name):
        """Add variable values to the url.
           (e.g. /your/api/{variable_value}/call)
           Another example: if you have a Python reserved word, such as global,
           in your url, you must use this method.

        :param name: Name of the url segment
        :type name: string
        :return: Client object
        """
        return self._build_client(name)

    def __getattr__(self, name):
        """Dynamically add method calls to the url, then call a method.
           (e.g. client.name.name.method())
           You can also add a version number by using .version(<int>)

        :param name: Name of the url segment or method call
        :type name: string or integer if name == version
        :return: mixed
        """
        if name == 'version':
            def get_version(*args, **kwargs):
                """
                :param args: dict of settings
                :param kwargs: unused
                :return: string, version
                """
                self._version = args[0]
                return self._build_client()
            return get_version

        # We have reached the end of the method chain, make the API call
        if name in self.methods:
            method = name.upper()

            def http_request(*args, **kwargs):
                """Make the API call
                :param args: unused
                :param kwargs:
                :return: Client object
                """
                if 'request_headers' in kwargs:
                    self._update_headers(kwargs['request_headers'])
                data = json.dumps(kwargs['request_body']).encode('utf-8')\
                    if 'request_body' in kwargs else None
                params = kwargs['query_params']\
                    if 'query_params' in kwargs else None
                opener = urllib.build_opener()
                request = urllib.Request(self._build_url(params), data=data)
                if self.request_headers:
                    for key, value in self.request_headers.items():
                        request.add_header(key, value)
                request.get_method = lambda: method
                return Response(self._make_request(opener, request))
            return http_request
        else:
            # Add a segment to the URL
            return self._(name)
