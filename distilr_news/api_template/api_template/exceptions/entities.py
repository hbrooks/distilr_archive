from .base import DistilrBaseException

class EntityNotFound(DistilrBaseException):
    def __init__(self, searched_by_key, searched_by_value):
        super().__init__(
            404,
            'Entity not found by searching for {} = {}'.format(searched_by_key, searched_by_value),
            {
                searched_by_key: searched_by_value
            }
        )
