class Error(Exception):
    '''Base class for libdinero exceptions

    :param message: textual description of exception
    '''

    message: str

class NotConnectedError(Error):
    '''Exception rasied when trying to authenticate a non-connected instance'''

    def __init__(self, message: str):
        self.message = message

class NotAuthenticatedError(Error):
    '''Exception rasied when trying to configure a non-authenticated instance'''

    def __init__(self, message: str):
        self.message = message

class NotConfiguredError(Error):
    '''Exception rasied when trying to do requests on a non-configured instance'''

    def __init__(self, message: str):
        self.message = message
