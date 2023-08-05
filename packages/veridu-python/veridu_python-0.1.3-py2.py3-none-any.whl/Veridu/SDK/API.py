from six.moves import urllib
import requests
import random
import time
import collections
import hashlib
import hmac

from Veridu.Exceptions.InvalidResponse import InvalidResponse
from Veridu.Exceptions.InvalidFormat import InvalidFormat
from Veridu.Exceptions.APIError import APIError
from Veridu.Exceptions.NonceMismatch import NonceMismatch

class API(object):

    def __init__(self, key, secret, version="0.3"):
        self.key = key
        self.secret = secret
        self.version = version
        self.session = None
        self.headers = {
            "Veridu-Client": key,
            "User-Agent": "Veridu-Python/0.1.3"
        }

    def setSession(self, session):
        self.session = session
        self.headers["Veridu-Session"] = session

    def getSession(self):
        return self.session

    def purgeSession(self):
        self.session = None
        self.headers.pop("Veridu-Session", None)

    def createSignature(self, method, url):
        self.nonce = ''.join([str(random.randint(0, 9)) for i in range(10)])
        rawPayload = {
            "client": self.key,
            "hash": "sha1",
            "method": method.upper(),
            "nonce": self.nonce,
            "resource": url,
            "timestamp": int(time.time()),
            "version": self.version
        }
        payload = urllib.parse.urlencode(collections.OrderedDict(sorted(rawPayload.items())))
        hmacInstance = hmac.new(self.secret.encode(), msg=payload.encode(), digestmod=hashlib.sha1)
        rawPayload["signature"] = hmacInstance.hexdigest()
        return rawPayload

    def fetch(self, method, resource, data=None):
        baseUrl = urllib.parse.urljoin("https://api.veridu.com", "/%s/%s" % (self.version, resource))

        if (method == "GET"):
            response = requests.get(baseUrl, params=data, headers=self.headers)
        elif (method == "POST"):
            response = requests.post(baseUrl, data=data, headers=self.headers)
        elif (method == "PUT"):
            response = requests.put(baseUrl, data=data, headers=self.headers)
        elif (method == "DELETE"):
            response = requests.delete(baseUrl, data=data, headers=self.headers)

        try:
            json = response.json()
            if "status" not in json:
                raise InvalidResponse(response.text)
            if json["status"] == False:
                self.lastError = json["error"]["type"]
                raise APIError(json["error"]["message"])
            return json
        except ValueError:
            raise InvalidFormat(response.text)


    def signedFetch(self, method, resource, data=None):
        sign = self.createSignature(
            method,
            urllib.parse.urljoin("https://api.veridu.com", "/%s/%s" % (self.version, resource))
        )

        if data is None:
            json = self.fetch(method, resource, sign)
        else:
            data.update(sign)
            json = self.fetch(method, resource, data)

        if "nonce" not in json or json["nonce"] != self.nonce:
            raise NonceMismatch()

        json.pop("nonce", None)
        return json
