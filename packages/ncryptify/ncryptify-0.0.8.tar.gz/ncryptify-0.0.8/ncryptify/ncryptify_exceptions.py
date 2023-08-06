class NcryptifyException(Exception):
    def __init__(self, message, status_code=-1):
        self.message = message
        self.status_code = status_code
    def __str__(self):
        if self.status_code is None:
            return repr(self.message)
        else:
            return repr(str(self.status_code) + ': ' + self.message)

class KeyNotFound(NcryptifyException):
    """raise this when a key is not found"""

class ErrorFetchingRandom(NcryptifyException):
    """raise this when unable to fetch random bytes"""


class KeyNotCreated(NcryptifyException):
    """raise this when a key could not be created"""


class KeyNotDeleted(NcryptifyException):
    """raise this when a key could not be deleted"""


class ErrorFetchingKey(NcryptifyException):
    """raise this when an unknown error occurs while creating or getting a key"""


class KeyAlreadyExists(NcryptifyException):
    """raise this when a create key request is made for the key that already exists"""


class AccountNotFound(NcryptifyException):
    """raise this when an account is not found"""

class InvalidKeyType(NcryptifyException):
    """raise this when encryption or decryption tries to use an FPE key"""

class HideRequestFailed(NcryptifyException):
    """raise this when a FPE hide request fails"""

class UnhideRequestFailed(NcryptifyException):
    """raise this when a FPE unhide request fails"""

