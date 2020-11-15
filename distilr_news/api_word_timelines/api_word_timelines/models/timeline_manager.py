import json
import logging
import random
import uuid
from uuid import uuid4
from datetime import datetime
from datetime import timedelta

import numpy as np
from flask import current_app

from ..exceptions import TimelineCreationNotAuthorized
from ..exceptions import TimelineNotFound
from .timeline import Timeline
from .timeline import Event
from .timeline import Concept
from .distilr_JSON_serializer import DistilrJsonSerializer
from .db_models import TimelinesRow

LOG = logging.getLogger(__name__)

class TimelineManager:

    TRENDING_CACHE_KEY = 'trending_concepts'
    TYPES_OF_TRENDING_CONCEPTS = ['person', 'org', 'loc']


    def __init__(self, event_registry_api_proxy, is_allowed_to_create):
        self.is_allowed_to_create = is_allowed_to_create
        self.er = event_registry_api_proxy


    def create(self, session, topic_concept, time_start, time_end, now):

        if self.is_allowed_to_create == False:
            raise TimelineCreationNotAuthorized()

        if time_start == None:
            time_start = now - timedelta(days=3)

        if time_end == None:
            time_end = now 

        events = self.er.get_events_from_uri(topic_concept.uri, time_start, time_end)

        timeline = Timeline(
            str(uuid4()),
            now,
            time_start,
            time_end,
            topic_concept,
            raw_content=events,
        )

        if Concept.from_uri(session, topic_concept.uri) == None:
            topic_concept.save(session)

        self._save(session, timeline)

        return timeline


    def _save(self, session, timeline):
        timeline_row = TimelinesRow(
            id=timeline.id,
            created_at=timeline.created_at,
            time_start=timeline.time_start,
            time_end=timeline.time_end,
            concept_uri=timeline.topic_concept.uri,
            content=json.dumps(timeline.content_to_dict())
        )
        session.add(timeline_row)


    def _build_timeline_from_timeline_row(self, timeline_row, concept):
        return Timeline(
            timeline_row.id,
            timeline_row.created_at,
            timeline_row.time_start,
            timeline_row.time_end,
            concept,
            processed_content=json.loads(timeline_row.content)
        )
        

    def get_timeline(self, session, concept, time_start, time_end):
        timeline_row = session.query(TimelinesRow).\
            filter(TimelinesRow.concept_uri == concept.uri).\
            filter(TimelinesRow.time_start == time_start).\
            filter(TimelinesRow.time_end == time_end).\
            first()
        if timeline_row == None:
            raise TimelineNotFound()
        return self._build_timeline_from_timeline_row(timeline_row, concept)


    def create_trending(self, cache):
        trending_concepts = self.er.fetch_trending_concepts()
        trending_concepts_response = {}
        for concept_type in self.TYPES_OF_TRENDING_CONCEPTS:
            if concept_type in trending_concepts:
                concepts = []
                for raw_concept in trending_concepts[concept_type]['trendingConcepts'][:5]:
                    concepts.append(Concept(
                        raw_concept['uri'],
                        raw_concept['type'],
                        None,
                        raw_concept['label']['eng']))
                trending_concepts_response[concept_type] = concepts
        # TODO: Create a type of object for trending concepts response
        LOG.info(trending_concepts_response)
        serialized_trending_concepts_response = {k: [c.to_dict() for c in v] for k,v in trending_concepts_response.items()}
        cache.set(self.TRENDING_CACHE_KEY, json.dumps(serialized_trending_concepts_response)) # TODO: put expiration time on the cache entry.
        return trending_concepts_response


    def get_trending(self, cache):
        cache_entry = cache.get(self.TRENDING_CACHE_KEY)
        if cache_entry == None:
            return None
        cache_entry_dict = json.loads(cache_entry)
        return {k: [Concept.from_dict(c) for c in v] for k,v in cache_entry_dict.items()}

