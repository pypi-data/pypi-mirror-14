class BaseException(Exception):
    """
    Base class for exceptions in this module.
    """
    def __init__(
            self, error_code, message, session_key=None,
            device=None, application=None):
        """
        Intializing exception class
        :params value: String message
        :params error_code: error code
        :params session_key: Loggedin user session key

        :returns: None
        """
        self.error_code = error_code
        self.session_key = session_key
        self.device = device
        self.application = application
        self.message = "%s- %s" % (self.error_code, message)

    def __str__(self):
        """
        Class level function to return representational view of
        class object

        :returns: Representational view of message
        """
        return repr(self.message)


class MultiLogginFound(BaseException):
    """
    Raised in case of user is logged in from
    multiple devices
    """
    pass


class InactiveSessionFound(BaseException):
    """
    Raised incase session is inactice since INACTIVE_SESSION_TIMEOUT
    """
    pass
