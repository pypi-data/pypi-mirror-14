import unittest

from prompt.classes.authentication.AuthenticationService import AuthenticationService
from prompt.classes.chat.Chat import Chat

from prompt.classes.apiEndpoint.ApiEndpoint import ApiEndpoint


class TestChat(unittest.TestCase):

    def setUp(self):
        authenticationService = AuthenticationService()
        authInfoResult = authenticationService.getAuthenticationInfo(cellphone="+5491162503829", password="1234")
        apiEndpoint = ApiEndpoint(authenticationInfo=authInfoResult.get("authInfo"))
        self.chat = Chat(apiEndpoint=apiEndpoint)

    def testRetrieveInitialChatNotEmpty(self):
        messages = self.chat.retrieveInitialChatThread()
        self.assertGreater(len(messages), 0)

    def testRetrievingListOfCommands(self):
        response = self.chat.sendMessage("/list")
        self.assertRegexpMatches(response, ".*@.*@.*")
