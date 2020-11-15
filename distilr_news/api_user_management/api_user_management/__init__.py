import json
import os
import logging

from flask import current_app
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .views import get_events_blueprint
from .views import get_users_blueprint
from .models import CacheConnectionManager
from .models import DatabaseConnectionManager
from .models import UserManager
from .models import EventManager
from .models import SessionManager
from .server_utilities import build_distilr_api


LOG = logging.getLogger(__name__)

def create_app_helper(
    database_connection_manager=None,
    cache_connection_manager=None,
    user_manager=None,
    event_manager=None,
    session_manager=None):

    if database_connection_manager == None:
        database_connection_manager = DatabaseConnectionManager({})
        # {
        #     field_name: os.environ[field_name] for field_name in [
        #         'POSTGRES_USER',
        #         'POSTGRES_PASSWORD',
        #         'POSTGRES_HOST_NAME',
        #         'POSTGRES_HOST_PORT',
        #         'POSTGRES_DB'
        #     ]
        # }
    
    if cache_connection_manager == None:
        cache_connection_manager = CacheConnectionManager({
            'host_name': 'redis_cache', # TODO: Get from an ENV VAR
            'port': 6379,  # TODO: Get from an ENV VAR
        })

    if event_manager == None:
        event_manager = EventManager()

    if user_manager == None:
        user_manager = UserManager(event_manager)

    if session_manager == None:
        session_manager = SessionManager(cache_connection_manager, user_manager)

    DB = SQLAlchemy()

    users_blueprint = get_users_blueprint(user_manager)
    events_blueprint = get_events_blueprint(user_manager, event_manager)

    def build_distilr_application_context():
        DB.init_app(current_app)

    def before_request_function(distilr_application_context):
        g.session = database_connection_manager.get_session()

    def health_check_function(_):
        database_connection_manager.validate_connection()
        cache_connection_manager.validate_connection()
        return '', 200

    return build_distilr_api(
        {
            users_blueprint,
            events_blueprint,
        },
        build_distilr_application_context=build_distilr_application_context,
        health_check_function=health_check_function,
        before_request_function=before_request_function,
    )


def create_app():
    """
    The production environment builds this Flask App via this method.
    """
    return create_app_helper()
