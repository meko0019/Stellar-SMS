from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix = '/api')

@api_blueprint.route('/health', methods=['GET'])
def health():

	return "I'm up! :)", 201