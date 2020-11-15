import requests

from api_distilr_news.exceptions import AccountCreationNotAuthorized
from api_distilr_news.exceptions import LoginDisallowed
from api_distilr_news.exceptions import SessionNotFound

from .distilr_microservice_utilities import DistilrMicroserviceUtilities

class UserManagementService:
    
    def __init__(self, base_api_url):
        self.base_api_url = base_api_url


    def is_connection_healthy(self):
        return DistilrMicroserviceUtilities.check_health(self.base_api_url)


    # def create_standard_user(self, email, password):
    #     def _handle_403(response_json):
    #         raise AccountCreationNotAuthorized(response_json['details']['email'])
    #     response_json = DistilrMicroserviceUtilities.make_request(
    #         'POST',
    #         self.base_api_url + '/users',
    #         {
    #             'email': email,
    #             'password': password
    #         },
    #         {
    #             403: _handle_403,
    #         }
    #     )
    #     return response_json['userId']


    def create_anonymous_user(self, address):
        response_json = DistilrMicroserviceUtilities.make_request(
            'POST',
            self.base_api_url + '/users',
            {
                'type': 'anonymous',
                'address': address
            },
            {},
        )
        return response_json['userId']


    def get_all_user_events(self, user_id):
        response_json = DistilrMicroserviceUtilities.make_request(
            'GET',
            self.base_api_url + '/events?userId={}'.format(user_id),
            {},
            {},
        )
        return response_json

    def create_timeline_requested_event(self, user_id):
        return self._create_event(
            user_id,
            'timeline_requested'
        )

    def create_timeline_creation_event(self, user_id):
        return self._create_event(
            user_id,
            'timeline_creation'
        )

    def _create_event(self, user_id, event_type):
        response_json = DistilrMicroserviceUtilities.make_request(
            'POST',
            self.base_api_url + '/events',
            {
                'userId': user_id,
                'eventType': event_type
            },
            {},
        )
        return response_json


    # def create_standard_session(self, email, password):
    #     def _handle_403(response_json):
    #         raise LoginDisallowed(response_json['details']['email'])
    #     response_json = DistilrMicroserviceUtilities.make_request(
    #         'POST',
    #         self.base_api_url + '/sessions',
    #         {
    #             'email': email,
    #             'password': password,
    #             'type': 'standard',
    #         },
    #         {
    #             403: _handle_403,
    #         }
    #     )
    #     return response_json['sessionId']

    # def get_session(self, session_id):
    #     def _handle_404(response_json):
    #         raise SessionNotFound(response_json['details']['session_id'])
    #     response_json = DistilrMicroserviceUtilities.make_request(
    #         'GET',
    #         self.base_api_url + '/sessions/{}'.format(session_id),
    #         None,
    #         {
    #             404: _handle_404,
    #         }
    #     )
    #     return response_json