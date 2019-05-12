from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/health', methods=['GET'])
def health():

	return "I'm up! :)", 201