__version__ = (1, 0, 0, "dev")

import json
import os
import logging
from werkzeug.utils import find_modules
import logging

from api_distilr_news.server_utilities import build_distilr_api
from .config.distilr_backend_apis import get_api_user_management_url
from .config.distilr_backend_apis import get_api_word_timelines_url
# from .views import get_users_blueprint
# from .views import get_search_blueprint
from .views import get_timelines_blueprint
from .models import WordTimelinesService
from .models import UserManagementService


LOG = logging.getLogger(__name__)


def create_app_helper(user_management_service, word_timelines_service):
    
    # users_blueprint = get_users_blueprint(user_management_service)
    # search_blueprint = get_search_blueprint(user_management_service, word_timelines_service)
    timelines_blueprint = get_timelines_blueprint(user_management_service, word_timelines_service)

    def health_check_function(_):
        # TODO: The current curl healthcheck command views 500s as successful calls.
        if not user_management_service.is_connection_healthy():
            return '', 500 
        elif not word_timelines_service.is_connection_healthy():
            return '', 500 
        else:
            return '', 200

    return build_distilr_api(
        {
            # users_blueprint,
            # search_blueprint,
            timelines_blueprint
        },
        health_check_function=health_check_function
    )


def create_app():
    user_management = UserManagementService(get_api_user_management_url())
    word_timelines_service = WordTimelinesService(get_api_word_timelines_url())
    return create_app_helper(
        user_management,
        word_timelines_service
    )