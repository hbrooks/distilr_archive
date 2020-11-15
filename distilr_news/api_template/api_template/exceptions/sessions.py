from .base import DistilrBaseException

class SessionNotFound(DistilrBaseException):
    def __init__(self, session_key, not_found_as_of):
        super().__init__(
            404,
            'Session with key={} not found.'.format(session_key),
            {
                'session_key': session_key,
                'not_found_as_of': not_found_as_of,
            }
        )
