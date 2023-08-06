from api_star.request import RequestMixin
from falcon.request import Request as _Request


class CaseInsensitiveDict(dict):
    """
    Falcon uses all uppercase values for the request headers.
    We'd like to ensure case-insensitive lookups, so that eg.
    `request.headers['Accept']` is valid.
    """
    def get(self, key, default=None):
        return super(CaseInsensitiveDict, self).get(key.upper(), default)


class Request(RequestMixin, _Request):
    @property
    def headers(self):
        if not hasattr(self, '_headers'):
            self._headers = CaseInsensitiveDict(super(Request, self).headers)
        return self._headers
