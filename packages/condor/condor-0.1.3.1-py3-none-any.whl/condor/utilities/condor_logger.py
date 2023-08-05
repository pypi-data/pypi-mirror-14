from colorama import init, Fore, Back, Style

class CondorLogger(object):
    """description of class"""

    def __init__(self):
        init()

    def log_warning(self, message):
        print(Fore.YELLOW + 'WARNING: ' + Style.RESET_ALL + message)

    def log_success(self, message):
        print(Fore.GREEN + 'SUCCESS: ' + Style.RESET_ALL + message)

    def log_error(self, message):
        print(Fore.RED + 'ERROR: ' + Style.RESET_ALL + message)

    def log_general(self, message):
        print(message)
        #print(self.terminal.yellow + 'WARNING: ' + self.terminal.normal + message)



