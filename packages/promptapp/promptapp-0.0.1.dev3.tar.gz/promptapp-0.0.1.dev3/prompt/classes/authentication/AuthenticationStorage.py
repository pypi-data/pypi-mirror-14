import os, json
from subprocess import call
from AuthenticationInfo import AuthenticationInfo

class AuthenticationStorage(object):

    def _getAuthinfoPath(self):
        return os.path.expanduser("~/.promptauth")

    def deleteAuthInfo(self):
        if os.path.isfile(self._getAuthinfoPath()):
            call(["rm", self._getAuthinfoPath()])

    def getAuthInfo(self):
        if not os.path.isfile(self._getAuthinfoPath()):
            return

        with open(self._getAuthinfoPath()) as authinfoFile:
            authinfoData = json.load(authinfoFile)
            authinfo = AuthenticationInfo()
            authinfo.uuid = authinfoData["uuid"]
            authinfo.access_token = authinfoData["access_token"]
            authinfo.expires_in = authinfoData["expires_in"]
            authinfo.token_type = authinfoData["token_type"]
            authinfo.scope = authinfoData["scope"]
            authinfo.refresh_token = authinfoData["refresh_token"]
            return authinfo

    def storeAuthInfo(self, authinfo):
        with open(self._getAuthinfoPath(), "w") as authinfoFile:
            json.dump(authinfo.__dict__, authinfoFile)