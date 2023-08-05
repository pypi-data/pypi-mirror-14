from requests import Request, Session
import urllib.parse

class HTTPException(Exception): pass

class HTTPClientException(HTTPException): pass
class HTTPBadRequest(HTTPClientException): pass
class HTTPUnauthorized(HTTPClientException): pass
class HTTPForbidden(HTTPClientException): pass
class HTTPNotFound(HTTPClientException): pass
class HTTPConflict(HTTPClientException): pass

class HTTPServerException(HTTPException): pass
class HTTPInternalServerError(HTTPServerException): pass
class HTTPNotImplemented(HTTPServerException): pass
class HTTPBadGateway(HTTPServerException): pass
class HTTPServiceUnavailable(HTTPServerException): pass
class HTTPGatewayTimeout(HTTPServerException): pass

status_code_exceptions = {
    400: HTTPBadRequest,
    401: HTTPUnauthorized,
    403: HTTPForbidden,
    404: HTTPNotFound,
    409: HTTPConflict,

    500: HTTPInternalServerError,
    501: HTTPNotImplemented,
    502: HTTPBadGateway,
    503: HTTPServiceUnavailable,
    504: HTTPGatewayTimeout,
}

def _null_intercept(request):
    return request

class PeaceMaker(object):
    def __init__(self, base):
        self.base = base

    def make(self, name, path=None, has={}, intercept=_null_intercept):
        def __init__(self, attributes={}, links={}, new=True):
            self.new        = new
            self.__setup__(attributes, links)

        def __setup__(self, attributes={}, links={}):
            self.__attributes__ = list(attributes.keys())
            for name in self.__attributes__:
                setattr(self, name, attributes[name])
            if isinstance(links, dict):
                self.__links__ = links
            elif isinstance(links, list):
                self.__links__ = {}
                for link in links:
                    self.__links__[link['rel']] = link

        def save(self):
            if self.new:
                session = Session()
                request = self.__class__.intercept(Request(
                    'POST',
                    self.__class__.__path__,
                    json={
                        name: getattr(self, name) for name in self.__attributes__
                    }
                ))
                response = session.send(session.prepare_request(request))
                try:
                    http_exception = status_code_exceptions[response.status_code]
                    raise http_exception
                except KeyError:
                    pass

                data = response.json()['data']
                self.new = False
                self.__attributes__.append('id')
                self.id = data['id']
            else:
                path = '{0}/{1}'.format(self.__class__.__path__.rstrip('/'), self.id)
                session = Session()
                request = self.__class__.intercept(Request(
                    'PUT',
                    path,
                    json={
                        name: getattr(self, name) for name in self.__attributes__
                    }
                ))
                response = session.send(session.prepare_request(request))
                try:
                    http_exception = status_code_exceptions[response.status_code]
                    raise http_exception
                except KeyError:
                    pass

        def refresh(self):
            session = Session()
            request = self.__class__.intercept(Request('GET', self.__links__['self']['href']))
            response = session.send(session.prepare_request(request))
            try:
                http_exception = status_code_exceptions[response.status_code]
                raise http_exception()
            except KeyError:
                content = response.json()
            self.__setup__(attributes=content['data'], links=content['links'])

        @classmethod
        def get(klass, id):
            session = Session()
            request = klass.intercept(Request('GET', '{0}/{1}'.format(klass.__path__.rstrip('/'), id)))
            response = session.send(session.prepare_request(request))
            try:
                http_exception = status_code_exceptions[response.status_code]
                raise http_exception()
            except KeyError:
                content = response.json()
            return klass(attributes=content['data'], links=content['links'])

        @classmethod
        def search(klass, **attributes):
            url = klass.__path__
            if len(attributes) > 0:
                url += '?' + urllib.parse.urlencode(attributes)
            session = Session()
            request = klass.intercept(Request('GET', url))
            response = session.send(session.prepare_request(request))
            return [klass(attributes=entry['data']) for entry in response.json()['data']]

        def __getattr__(self, name):
            if name not in self.__dict__:
                self.refresh()
            try:
                return self.__dict__[name]
            except KeyError:
                raise AttributeError("'{0}' object has not attribute '{1}'".format(self.__class__.__name__, name))

        methods = {
            '__init__': __init__,
            '__setup__': __setup__,
            'save':     save,
            'refresh':  refresh,
            'get':      get,
            'search':   search,
            '__path__': urllib.parse.urljoin(self.base, path),
            '__getattr__': __getattr__,
            'intercept': intercept,
        }
        for name, kind in has.items():
            def follow_link(s, link_name):
                link    = s.__links__[link_name]
                data    = link['data'] if 'data' in link else {}
                links   = link['links'] if 'links' in link else {}
                if 'self' not in links:
                    links['self'] = {'href': link['href']}
                return kind(attributes=data, links=links)
            methods[name] = property(lambda s: follow_link(s, name), None)

        return type(name, (object,), methods)
