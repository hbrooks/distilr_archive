from datetime import datetime
import logging
import json

from flask import Flask
from flask import request
from flask import Blueprint
from flask import jsonify

from api_word_timelines.request_utilities import request_is_json
from api_word_timelines.request_utilities import get_required_field
from ..exceptions import TimelineNotFound
from ..exceptions import NotEnoughDataToCreateTimeline

LOG = logging.getLogger(__name__)

def get_timelines_blueprint(database_connection_manager, cache_connection_manager, event_registry_api_proxy, timeline_manager):
    
    timelines_blueprint = Blueprint('timelines', __name__, url_prefix='/timelines')

    @timelines_blueprint.route("", methods=('POST',))
    @request_is_json
    def create_timeline():

        q = get_required_field(request.json, 'q')
        time_end = request.json.get('timeEnd', None)
        if time_end != None:
            time_end = datetime.fromordinal(time_end)
        time_start = request.json.get('timeStart', None)
        if time_start != None:
            time_start = datetime.fromordinal(time_start)
        should_create_if_not_found = request.json.get('shouldCreateIfNotFound', False)

        concept = event_registry_api_proxy.get_concept(q)
        if concept == None:
            raise TimelineNotFound()

        session = database_connection_manager.get_session()
        try:
            timeline = timeline_manager.get_timeline(session, concept, time_start, time_end)
        except TimelineNotFound as e:
            if should_create_if_not_found:
                try:
                    timeline = timeline_manager.create(session, concept, time_start, time_end, datetime.now()) 
                except NotEnoughDataToCreateTimeline as e:
                    return {}, 406
                session.commit()   
            else:
                raise e
        return timeline.to_json(), 200

    @timelines_blueprint.route("/trending", methods=('GET',))
    def get_trending():
        cache = cache_connection_manager.get_connection()
        trending_concepts = timeline_manager.get_trending(cache)
        if trending_concepts == None:
            trending_concepts = timeline_manager.create_trending(cache)
        return {k: [e.to_dict() for e in v] for k,v in trending_concepts.items()}, 200

    return timelines_blueprint