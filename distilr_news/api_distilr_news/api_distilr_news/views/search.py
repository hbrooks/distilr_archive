# from datetime import datetime
# import logging

# from flask import Blueprint
# from flask import request
# from flask import jsonify


# from api_distilr_news.request_utilities import request_is_json
# from api_distilr_news.request_utilities import get_required_field

# LOG = logging.getLogger(__name__)

# def get_search_blueprint(user_management_service, word_timelines_service):
#     """
#     GET /search?q=Apple
#         -   Returns a list of entities that relate to `q`. No log in required.
#     """
#     search_blueprint = Blueprint('search', __name__, url_prefix='/search')

#     @search_blueprint.route("", methods=('GET',))
#     def search():
#         query_string = get_required_field(request.args, 'q')
#         results = word_timelines_service.search_entities(query_string)
#         return jsonify(results), 200

#     return search_blueprint

