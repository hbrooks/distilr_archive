__version__ = (1, 0, 0, "dev")

import json
import os
import logging
from werkzeug.utils import find_modules
import logging

from flask import current_app
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from api_word_timelines.server_utilities import build_distilr_api
from .models import EventRegistryApiProxy
from .models import TimelineManager
from .models import DatabaseConnectionManager
from .models import CacheConnectionManager
from .views import get_timelines_blueprint
# from .views import get_entities_blueprint


LOG = logging.getLogger(__name__)

def create_app_helper(
    database_connection_manager,
    cache_connection_manager,
    event_registry_api_proxy,
    timeline_manager):

    DB = SQLAlchemy()

    timelines_blueprint = get_timelines_blueprint(database_connection_manager, cache_connection_manager, event_registry_api_proxy, timeline_manager)
    # entities_blueprint = get_entities_blueprint(database_connection_manager, bing_api)

    def build_distilr_application_context():
        DB.init_app(current_app)

    def before_request_function(distilr_application_context):
        g.session = database_connection_manager.get_session()

    def health_check_function(g): # TODO: Is g needed?
        is_healthy = True
        try:
            database_connection_manager.validate_connection()
        except Exception:
            LOG.info("MYSQL connection failed.")
            is_healthy = False

        try:
            cache_connection_manager.validate_connection()
        except Exception:
            LOG.info("Redis connection failed.")
            is_healthy = False
        if is_healthy:
            return '', 200
        else:
            return '', 500
        

    return build_distilr_api(
        {
            timelines_blueprint,
            # entities_blueprint,
        },
        build_distilr_application_context=build_distilr_application_context,
        health_check_function=health_check_function,
        before_request_function=before_request_function,
    )

def create_app():

    # TODO: source the connection from env vars
    database_connection_manager = DatabaseConnectionManager({})

    # TODO: source the connection from env vars
    cache_connection_manager = CacheConnectionManager({
        'host_name': 'redis_cache',
        'port': 6379,
    })

    event_registry_api_proxy = EventRegistryApiProxy(
        os.environ['EVENT_REGISTIRY_API_KEY'],
    )
    timeline_manager = TimelineManager(
        event_registry_api_proxy,
        True
    )
    
    return create_app_helper(
        database_connection_manager,
        cache_connection_manager,
        event_registry_api_proxy,
        timeline_manager,
    )