from Message import Message

class Chat(object):

    def __init__(self, apiEndpoint):
        self.apiEndpoint = apiEndpoint

    def retrieveInitialChatThread(self):
        return self.retrieveChatThread(limit=20)

    """
    Returns the chat thread limited to the provided parameters, as a list of Message
    fromDate and toDate must be in ISO 8601 format
    start and limit must be integers
    """
    def retrieveChatThread(self, botIdentifier = None, fromDate = None, toDate = None, start = None, limit = None):
        params = {}
        if botIdentifier:
            params["identifier"] = botIdentifier
        if fromDate:
            params["fromdate"] = fromDate
        if toDate:
            params["todate"] = toDate
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit

        result = self.apiEndpoint.get("ui/getchatthread/", params)

        messages = []
        for message in result["data"]["messages"]:
            msgObj = Message()
            msgObj.chatthreadid = message["chatthreadid"]
            msgObj.created = message["created"]
            msgObj.identifier = message["identifier"]
            msgObj.message = message["message"]
            msgObj.origin = message["origin"]
            messages.append(msgObj)

        return messages

    def sendMessage(self, message):
        result = self.apiEndpoint.get("messaging/web/", {"message": message})
        return result["data"]["textmessage"]
