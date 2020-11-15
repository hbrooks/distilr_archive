from datetime import datetime
import logging

from flask import Blueprint
from flask import request
from flask import jsonify

from ..exceptions import TimelineCreationNotAuthorized
from ..exceptions import TimelineNotFound
from ..exceptions import NotEnoughDataToCreateTimeline
from api_distilr_news.request_utilities import request_is_json
from api_distilr_news.request_utilities import get_required_field


LOG = logging.getLogger(__name__)


def get_timelines_blueprint(user_management_service, word_timelines_service):
    """
    POST timelines
        -   Creates or returns a timeline with the proper topicEntityId, timeStart, timeEnd
    """
    timelines_blueprint = Blueprint('timelines', __name__, url_prefix='/timelines')

    @timelines_blueprint.route("", methods=('POST',))
    def create_entity():

        q = get_required_field(request.json, 'q')

        # POST /users to give location and get userId
        user_id = user_management_service.create_anonymous_user(request.access_route[-1])

        # GET /events with userId
        user_events = user_management_service.get_all_user_events(user_id)

        should_create_if_not_found = True # TODO:

        now_ordinal = datetime.now().toordinal()
        try:
            timeline = word_timelines_service.create_timeline(q, now_ordinal - 7, now_ordinal, should_create_if_not_found)
            return timeline, 200
        except NotEnoughDataToCreateTimeline:
            return {}, 406


    @timelines_blueprint.route("/trending", methods=('GET',))
    def get_trending():
        trending_timelines = word_timelines_service.get_trending()
        return trending_timelines, 200

    return timelines_blueprint

