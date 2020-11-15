import requests
import logging


from .distilr_microservice_utilities import DistilrMicroserviceUtilities
from ..exceptions import TimelineCreationNotAuthorized
from ..exceptions import TimelineNotFound
from ..exceptions import NotEnoughDataToCreateTimeline


LOG = logging.getLogger(__name__)


class WordTimelinesService:
    
    def __init__(self, base_api_url):
        self.base_api_url = base_api_url

    def is_connection_healthy(self):
        return DistilrMicroserviceUtilities.check_health(self.base_api_url)

    def search_entities(self, query):
        response_json = DistilrMicroserviceUtilities.make_request(
            'GET',
            self.base_api_url + '/entities?q={}'.format(query),
            {},
            {}
        )
        return response_json

    def create_timeline(self, q, time_start, time_end, should_create_if_not_found):
        def _handle_403(response_body):
            raise TimelineCreationNotAuthorized()
        def _handle_406(response_body):
            raise NotEnoughDataToCreateTimeline()
        exception_handlers = {
            403: _handle_403,
            406: _handle_406,
        }
        if not should_create_if_not_found:
            def _handle_404(response_body):
                raise TimelineNotFound()
            exception_handlers[404]: _handle_404
        response_json = DistilrMicroserviceUtilities.make_request(
            'POST',
            self.base_api_url + '/timelines',
            {
                'q': q,
                'timeStart': time_start,
                'timeEnd': time_end,
                'shouldCreateIfNotFound': should_create_if_not_found
            },
            exception_handlers
        )
        return response_json

    def get_trending(self):
        response_json = DistilrMicroserviceUtilities.make_request(
            'GET',
            self.base_api_url + '/timelines/trending',
            {},
            {}
        )
        return response_json
