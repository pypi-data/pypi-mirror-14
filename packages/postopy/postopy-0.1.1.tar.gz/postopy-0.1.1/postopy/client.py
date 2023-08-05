import json
from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urlencode
from postopy.config import *
from postopy.exception import PostoError


class Client(object):
    def __init__(self, access_keys):
        self.ACCESS_KEYS = access_keys

    def get(self, uri, **kw):
        return self.execute(uri, 'GET', **kw)

    def post(self, uri, **kw):
        return self.execute(uri, 'POST', **kw)

    def put(self, uri, **kw):
        return self.execute(uri, 'PUT', **kw)

    def delete(self, uri, **kw):
        return self.execute(uri, 'DELETE', **kw)

    def execute(self, uri, http_verb, extra_headers=None, **kw):
        if not ('app_id' in self.ACCESS_KEYS and 'token' in self.ACCESS_KEYS):
            raise PostoError('Missing connection credentials %s' % self.ACCESS_KEYS)

        url = uri if uri.startswith(API_ROOT) else API_ROOT + uri

        data = kw or {}

        if http_verb == 'GET' and data:
            url += '?%s' % urlencode(data)
            data = {}

        data.update(self.ACCESS_KEYS)
        data = urlencode(data).encode('utf-8')

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',

            # Need to have user-agent header because API is behind CloudFlare
            # and CloudFlare will block requests without user-agent header
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/38.0',
        }
        headers.update(extra_headers or {})

        request = Request(url, data, headers)

        request.get_method = lambda: http_verb

        try:
            response = urlopen(request, timeout=CONNECTION_TIMEOUT)
        except HTTPError as e:
            raise PostoError(e.read())

        return json.loads(response.read().decode('utf-8'))
