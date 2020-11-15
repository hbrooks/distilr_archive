from .base import DistilrBaseException

class TimelineNotFound(DistilrBaseException):
    def __init__(self):
        super().__init__(
            404,
            'Timeline not found.',
            {}
        )

class TimelineCreationNotAuthorized(DistilrBaseException):
    def __init__(self):
        super().__init__(
            403,
            'Timeline creation not authorized.',
            {}
        )

class NotEnoughDataToCreateTimeline(DistilrBaseException):
    def __init__(self):
        super().__init__(
            404,
            'Timeline creation failed.',
            {}
        )
