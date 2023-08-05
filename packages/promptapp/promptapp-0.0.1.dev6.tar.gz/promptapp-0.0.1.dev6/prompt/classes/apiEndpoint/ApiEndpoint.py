import requests


class ApiEndpoint(object):

    def __init__(self, authenticationInfo = None):
        self.endpoint = "http://api.dev.promptapp.io/api/1.0/"
        self.authenticationInfo = authenticationInfo

    def get(self, url, params):
        if self.authenticationInfo:
            params["uuid"] = self.authenticationInfo.uuid
            params["utoken"] = self.authenticationInfo.access_token
        r = requests.get(self.endpoint + url, params=params)
        return r.json()

    def post(self, url, data):
        r = requests.post(self.endpoint + url, data=data)
        return r.json()
