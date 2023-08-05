from classes.authentication.AuthenticationService import AuthenticationService
from classes.apiEndpoint.ApiEndpoint import ApiEndpoint
from classes.chat.Chat import Chat

def main():
    print("Welcome to Prompt\n")

    authService = AuthenticationService()
    authInfo = authService.getCachedAuthenticationInfo()
    if not authInfo:
        cellphone = raw_input("Please enter your cellphone. A valid US number is +12123456789\n")
        success_registering = authService.registerUser(cellphone)
        if not success_registering:
            password = raw_input("Please enter your password:\n")
            authService.getAuthenticationInfo(cellphone, password)

        authInfo = authService.getCachedAuthenticationInfo()

    message = ""
    apiEndpoint = ApiEndpoint(authInfo)
    chat = Chat(apiEndpoint)

    print("")
    while True:
        message = raw_input("Please enter the message you want to send, then press enter. To exit, send Q\n")
        print("")
        if message.upper() == "Q":
            break
        print(chat.sendMessage(message))
        print("")

main()