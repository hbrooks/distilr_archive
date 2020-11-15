# from datetime import datetime
# import logging
# import json

# from flask import Flask
# from flask import request
# from flask import Blueprint
# from flask import jsonify

# from api_word_timelines.request_utilities import request_is_json
# from api_word_timelines.request_utilities import get_required_field
# from ..exceptions import TimelineNotFound


# LOG = logging.getLogger(__name__)


# def get_entities_blueprint(database_connection_manager, bing_api):
    
#     entities_blueprint = Blueprint('entities', __name__, url_prefix='/entities')

#     @entities_blueprint.route("", methods=('GET',))
#     @request_is_json
#     def search_for_entity():

#         query_string = get_required_field(request.args, 'q')

#         bing_entity = bing_api.search_entities(query_string)

#         return jsonify(bing_entity.to_dict()), 200

#     return entities_blueprint