import unittest

from classes.authentication.AuthenticationService import AuthenticationService
from classes.chat.Chat import Chat

from prompt.classes.apiEndpoint import ApiEndpoint


class TestChat(unittest.TestCase):

    def setUp(self):
        authenticationService = AuthenticationService()
        apiEndpoint = ApiEndpoint(authenticationInfo=authenticationService.getAuthenticationInfo(cellphone="+5491162503829", password="1234"))
        self.chat = Chat(apiEndpoint=apiEndpoint)

    def testRetrieveInitialChatNotEmpty(self):
        messages = self.chat.retrieveInitialChatThread()
        self.assertGreater(len(messages), 0)

    def testRetrievingListOfCommands(self):
        response = self.chat.sendMessage("/list")
        self.assertRegexpMatches(response, ".*@.*@.*")
