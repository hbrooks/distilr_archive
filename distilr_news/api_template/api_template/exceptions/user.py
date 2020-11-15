from .base import DistilrBaseException

class AccountCreationNotAuthorized(DistilrBaseException):
    def __init__(self, email):
        super().__init__(
            403,
            'Not allowed to create account for {}.'.format(email),
            {
                'email': email
            }
        )

class UserNotFound(DistilrBaseException):
    def __init__(self, lookup_key, lookup_value):
        super().__init__(
            404,
            'User ({}={}) not found.'.format(lookup_key, lookup_value),
            {
                'lookup_key': lookup_value
            }
        )

class LoginDisallowed(DistilrBaseException):
    def __init__(self, email):
        super().__init__(
            403,
            'Login disallowed for {}'.format(email),
            {
                'email': email,
            }
        )
