import unittest

from prompt.classes.authentication.AuthenticationService import AuthenticationService


class TestAuthenticationService(unittest.TestCase):

    def testLogin(self):
        authService = AuthenticationService()
        authService.deleteCachedAuthenticationInfo()

        self.assertIsNone(authService.getCachedAuthenticationInfo())

        result = authService.registerUser("+5491162503829")
        self.assertFalse(result)

        authinfo = authService.getAuthenticationInfo("+5491162503829", "1234")
        self.assertIsNotNone(authinfo.access_token)
        self.assertIsNotNone(authinfo.expires_in)
        self.assertIsNotNone(authinfo.refresh_token)
        self.assertIsNotNone(authinfo.token_type)
        self.assertIsNotNone(authinfo.uuid)

        self.assertIsNotNone(authService.getCachedAuthenticationInfo())

        authService.deleteCachedAuthenticationInfo()