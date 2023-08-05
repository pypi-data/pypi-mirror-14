import re

from Veridu.Exceptions.EmptySession import EmptySession
from Veridu.Exceptions.InvalidUsername import InvalidUsername

class Session(object):
    def __init__(self, api):
        self.api = api
        self.token = None
        self.expires = -1
        self.username = None

    def setToken(self, token):
        self.token = token

    def getToken(self):
        return self.token

    def setExpires(self, expires):
        self.expires = expires

    def getExpires(self):
        return self.expires

    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username

    def create(self, readOnly=False):
        if readOnly:
            json = self.api.signedFetch("POST", "session/read")
        else:
            json = self.api.signedFetch("POST", "session/write")

        self.api.setSession(json["token"])
        self.setToken(json["token"])
        self.setExpires(json["expires"])

    def extend(self):
        if self.token is None:
            raise EmptySession()
        json = self.api.signedFetch("PUT", "session/%s" % self.token)
        self.setExpires(json["expires"])

    def expire(self):
        if self.token is None:
            raise EmptySession()
        json = self.api.signedFetch("DELETE", "session/%s" % self.token)
        self.api.purgeSession()
        self.setExpires(-1)
        self.setUsername(None)

    def assign(self, username):
        if self.token is None:
            raise EmptySession()

        if not re.match("^[a-zA-Z0-9_-]+$", username):
            raise InvalidUsername()

        self.api.signedFetch("POST", "user/%s" % username)
        self.setUsername(username)
