from datetime import datetime
import logging
import os

from flask import Flask
from flask import current_app
from flask import g
from flask import request
from flask import Blueprint

from api_user_management.request_utilities import request_is_json
from api_user_management.request_utilities import get_required_field
from ..models import SessionManager

LOG = logging.getLogger(__name__)


def get_sessions_blueprint(cache_connection_manager, session_manager, user_manager):

    sessions_blueprint = Blueprint('sessions', __name__, url_prefix='/sessions')

    @sessions_blueprint.route("", methods=('POST',))
    @request_is_json
    def create_session():
        request_json = request.json
        email = get_required_field(request_json, 'email')
        password = get_required_field(request_json, 'password')
        session = g.session

        user = user_manager.attempt_login(session, email, password)

        session_id = session_manager.create(session, user, datetime.now().timestamp())
        return {
            'sessionId': session_id
        }, 200

    @sessions_blueprint.route("/<session_id>", methods=('GET',))
    def get_session(session_id):
        session_contents = session_manager.get(session_id, datetime.now().timestamp())
        return session_contents, 200

    return sessions_blueprint