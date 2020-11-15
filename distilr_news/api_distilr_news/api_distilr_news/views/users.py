# from datetime import datetime
# import logging

# from flask import Flask
# from flask import g
# from flask import request
# from flask import Blueprint

# from api_distilr_news.request_utilities import request_is_json
# from api_distilr_news.request_utilities import get_required_field

# LOG = logging.getLogger(__name__)

# DEFAULT_PASSWORD = 'readytolearn'

# def get_users_blueprint(user_management_service):
#     """
#     POST /users
#         -   Creates a user.
#     POST /login
#         -   Creates or gets a session for a user.
    
#     """
#     users_blueprint = Blueprint('users', __name__, url_prefix='/users')

#     @users_blueprint.route("", methods=('POST',))
#     @request_is_json
#     def create_user():

#         request_json = request.json

#         type = get_required_field(request_json, 'type')

#         if type == 'anonymous':
#             user_id = user_management_service.create_anonymous_user(request.access_route[-1])
#             return '', 200

#         elif type == 'standard':
#             email = get_required_field(request_json, 'email')
#             # NOTE: using a default password for everyone.
#             get_required_field(request_json, 'password')
#             password = DEFAULT_PASSWORD
#             user_id = user_management_service.create_standard_user(email, password)
#             return _create_standard_session(email, password)

#         else:
#             return '', 400


#     @users_blueprint.route("/login", methods=('POST',))
#     @request_is_json
#     def log_in_user():
#         request_json = request.json
#         email = get_required_field(request_json, 'email')
#         get_required_field(request_json, 'password')
#         return _create_standard_session(email, DEFAULT_PASSWORD)
        

#     def _create_standard_session(email, password):
#         session_id = user_management_service.create_standard_session(
#             email,
#             password,
#         )
#         return {
#             'sessionId': session_id,
#         }, 200

#     return users_blueprint
