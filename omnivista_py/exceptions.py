class APIClientError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message=None):
        super().__init__(message)
        self.message = message

class AuthenticationError(APIClientError):
    """Exception raised for authentication-related errors."""
    def __init__(self, message=None):
        super().__init__(message)

class DeviceRetrievalError(APIClientError):
    """Exception raised when retrieving devices fails."""
    def __init__(self, message=None):
        super().__init__(message)

class LoginError(APIClientError):
    """Exception raised when login fails."""
    def __init__(self, message=None):
        super().__init__(message)