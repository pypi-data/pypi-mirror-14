from AuthenticationInfo import AuthenticationInfo
from AuthenticationStorage import AuthenticationStorage
from prompt.classes.apiEndpoint.ApiEndpoint import ApiEndpoint


class AuthenticationService(object):

    def deleteCachedAuthenticationInfo(self):
        authStorage = AuthenticationStorage()
        authStorage.deleteAuthInfo()

    """Returns an AuthenticationInfo instance on success, else None"""
    def getCachedAuthenticationInfo(self):
        authStorage = AuthenticationStorage()
        return authStorage.getAuthInfo()

    def getAuthenticationInfo(self, cellphone, password):
        apiEndpoint = ApiEndpoint()
        result = apiEndpoint.get("ui/oauthlogin", {"cellphone": cellphone, "localpasswd": password})

        authInfo = AuthenticationInfo()
        authInfo.access_token = result["access_token"]
        authInfo.expires_in = result["expires_in"]
        authInfo.token_type = result["token_type"]
        authInfo.scope = result["scope"]
        authInfo.refresh_token = result["refresh_token"]
        authInfo.uuid = result["uuid"]

        authStorage = AuthenticationStorage()
        authStorage.storeAuthInfo(authInfo)

        return authInfo

    def registerUser(self, cellphone):
        apiEndpoint = ApiEndpoint()
        result = apiEndpoint.post("ui/registeruser", {"cellphone": cellphone})

        if result["data"]["created"]:
            authInfo = AuthenticationInfo()
            authInfo.access_token = result["oauth"]["access_token"]
            authInfo.expires_in = result["oauth"]["expires_in"]
            authInfo.token_type = result["oauth"]["token_type"]
            authInfo.scope = result["oauth"]["scope"]
            authInfo.refresh_token = result["oauth"]["refresh_token"]
            authInfo.uuid = result["oauth"]["uuid"]

            authStorage = AuthenticationStorage()
            authStorage.storeAuthInfo(authInfo)

        return result["data"]["created"]