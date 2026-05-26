from NetworkCheckFunction import NetworkCheckFunction
from AccountsCheckFunction import AccountsCheckFunction
from PrintFunction import PrintFunction

def main():
    NCF_return = NetworkCheckFunction()
    if NCF_return == -1:
        PrintFunction(2, "NoWifiConnection")
        return
    elif NCF_return == 0:
        PrintFunction(6, "NoInternetConnection")
        return
    elif NCF_return == 1:
        PrintFunction(3, "Redirected")
    else:
        PrintFunction(1, "NetworkIsOk")
        return
    
    ACF_return = AccountsCheckFunction()
    if ACF_return == "NULL":
        PrintFunction(4, "LoginFail")
        return
    else:
        PrintFunction(5, ACF_return)
        return
    
if __name__ == "__main__":
    main()