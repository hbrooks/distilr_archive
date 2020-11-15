from .base import DistilrBaseException

class NoSuchKey(DistilrBaseException):
    def __init__(self, key_name, o):
        self.description = 'Expected to find {} in {}'.format(key_name, o)
        self.status_code = 400
        self.details = None
