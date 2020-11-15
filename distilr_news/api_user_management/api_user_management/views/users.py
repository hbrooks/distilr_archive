from datetime import datetime
import logging

from flask import Flask
from flask import g
from flask import jsonify
from flask import request
from flask import Blueprint

from api_user_management.request_utilities import request_is_json
from api_user_management.request_utilities import get_required_field
from ..exceptions import AccountCreationNotAuthorized

LOG = logging.getLogger(__name__)

def get_users_blueprint(user_manager):
    
    users_blueprint = Blueprint('users', __name__, url_prefix='/users')

    @users_blueprint.route("", methods=('POST',))
    @request_is_json
    def create_user():

        request_json = request.json

        type = get_required_field(request_json, 'type')

        if type == 'anonymous':
            address = get_required_field(request_json, 'address')
            user = user_manager.create_anonymous_user(g.session, address)
            g.session.commit()
            return jsonify({
                'userId': user.id,
            }), 200
        
        elif type == 'standard':
            # email = get_required_field(request_json, 'email')
            # password = get_required_field(request_json, 'password')
            # user = user_manager.create_standard_user(g.session, email, password)
            return '', 400

        else:
            return '', 400


    return users_blueprint
