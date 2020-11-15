import json
import logging
from datetime import datetime

from .distilr_JSON_serializer import DistilrJsonSerializer
from .db_models import BingEntitiesRow

LOG = logging.getLogger(__name__)


class BingEntity:
    
    def __init__(self, id, name, description, presentation_info, image):
        self.id = id
        self.name = name
        self.description = description
        self.presentation_info = presentation_info
        self.image = image

    def save(self, session):
        bing_entities_row = BingEntitiesRow(
            id=self.id,
            description=self.description,
            name=self.name,
            presentation_info=self.presentation_info,
            image=self.image,
        )
        session.add(bing_entities_row)
