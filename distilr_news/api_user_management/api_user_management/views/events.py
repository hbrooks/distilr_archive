from datetime import datetime
import logging

from flask import Flask
from flask import g
from flask import jsonify
from flask import request
from flask import Blueprint

from api_user_management.request_utilities import request_is_json
from api_user_management.request_utilities import get_required_field
from ..models import EventManager


LOG = logging.getLogger(__name__)

def get_events_blueprint(user_manager, event_manager):
    events_blueprint = Blueprint('events', __name__, url_prefix='/events')

    @events_blueprint.route("", methods=('POST',))
    @request_is_json
    def create_events_view():

        user_id = get_required_field(request.json, 'userId')
        event_type = get_required_field(request.json, 'eventType')

        session = g.session

        user = user_manager.get_by_user_id(
            session,
            user_id
        )

        event = event_manager.create_generic_event(
            session,
            user_id,
            event_type,
            datetime.now()

        )
        session.commit()
        return jsonify(event.to_external_dict()), 200

    @events_blueprint.route("", methods=('GET',))
    def get_events():

        user_id = get_required_field(request.args, 'userId')

        session = g.session
        user_manager.get_by_user_id(
            session,
            user_id
        )

        events = event_manager.get_all(
            session,
            user_id,
        )

        return jsonify([e.to_external_dict() for e in events]), 200

    return events_blueprint