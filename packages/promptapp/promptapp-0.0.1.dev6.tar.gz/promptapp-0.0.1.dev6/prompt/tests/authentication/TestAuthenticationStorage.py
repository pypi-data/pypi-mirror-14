import os
import unittest

from prompt.classes.authentication.AuthenticationInfo import AuthenticationInfo

from prompt.classes.authentication.AuthenticationStorage import AuthenticationStorage


class TestAuthenticationStorage(unittest.TestCase):

    def _deleteAuthInfoFile(self):
        authStorage = AuthenticationStorage()
        authStorage.deleteAuthInfo()

    def _getAuthinfoSeed(self):
        authinfo = AuthenticationInfo()
        authinfo.uuid = "82b8f880148db12dcdb30135b892ab8cddc6fcd25e1f24e140d66fdf38972bee"
        authinfo.access_token = "a6885627d2e970532eac96bc2eaec0b2d2285dedff6d0e41e1b3de962a4e5719"
        authinfo.expires_in = 2592000
        authinfo.token_type = "Bearer"
        authinfo.scope = None
        authinfo.refresh_token = "21fa0ac325de82b3c1f03f75f0d59fddd813966fcfa14492bb6bef7d463a3e9e"
        return authinfo

    def testEmptyFile(self):
        self._deleteAuthInfoFile()
        authStorage = AuthenticationStorage()
        authInfo = authStorage.getAuthInfo()

        self.assertIsNone(authInfo)

    def testNotEmptyFile(self):
        authStorage = AuthenticationStorage()
        authStorage.storeAuthInfo(self._getAuthinfoSeed())
        authInfo = authStorage.getAuthInfo()

        self.assertEqual("82b8f880148db12dcdb30135b892ab8cddc6fcd25e1f24e140d66fdf38972bee", authInfo.uuid)
        self.assertEqual("a6885627d2e970532eac96bc2eaec0b2d2285dedff6d0e41e1b3de962a4e5719", authInfo.access_token)
        self.assertEqual(2592000, authInfo.expires_in)
        self.assertEqual("Bearer", authInfo.token_type)
        self.assertIsNone(authInfo.scope)
        self.assertEqual("21fa0ac325de82b3c1f03f75f0d59fddd813966fcfa14492bb6bef7d463a3e9e", authInfo.refresh_token)

        self._deleteAuthInfoFile()

    def testStoreAuthinfo(self):
        authStorage = AuthenticationStorage()
        self._deleteAuthInfoFile()

        self.assertFalse(os.path.isfile(authStorage._getAuthinfoPath()))

        authinfo = self._getAuthinfoSeed()

        authStorage.storeAuthInfo(authinfo)

        self.assertTrue(os.path.isfile(authStorage._getAuthinfoPath()))

        authinfoPersisted = authStorage.getAuthInfo()

        self.assertDictEqual(authinfo.__dict__, authinfoPersisted.__dict__)

        self._deleteAuthInfoFile()