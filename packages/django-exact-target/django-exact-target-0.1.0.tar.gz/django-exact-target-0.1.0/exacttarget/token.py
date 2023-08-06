from collections import namedtuple
from django.core.cache import cache
import requests
import time
from . import settings

Token = namedtuple('Token', ('token', 'referenceTimestamp', 'expiresIn'))


class TokenGenerator(object):
    client_id = settings.EXACT_TARGET_CLIENT_ID
    client_secret = settings.EXACT_TARGET_CLIENT_SECRET
    url = 'https://auth.exacttargetapis.com/v1/requestToken'

    def generate(self):
        t = self._request()
        return t.token

    def headers(self):
        headers = {
            'Authorization': 'Bearer %s' % self.generate()
        }
        return headers

    def _request(self):
        resp = requests.post(self.url, json={
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        })

        resp.raise_for_status()
        data = resp.json()
        token = Token(
            token=data.get("accessToken"),
            referenceTimestamp=time.time(),
            expiresIn=data.get("expiresIn"))
        return token


class CachedTokenGenerator(TokenGenerator):
    tolerance = 10 # Cache the token for 10 seconds less than it's valid

    def _gen_key(self):
        return 'exacttarget_%s' % self.client_id

    def _request(self):
        key = self._gen_key()
        token = cache.get(key)
        if token is None:
            token = super()._request()
            cache.set(key, token, token.expiresIn - self.tolerance)
        return token
