import json
from flask import request, Blueprint, abort

from client.users.models import User
from client.api.json_models._query import JSONModelQueryBuilder
from client.api.json_models._create import JSONModelCreator
from client.database import db, execute_query

from client.api import APIException

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
    	result = User.query.get(user_id).__json__()
    except AttributeError as e:
    	return f"Error: User with id {user_id} does not exist.", 404
    return str(result), 200

@users_blueprint.route('/users', methods=['GET'])
def get_users():
	builder = JSONModelQueryBuilder(User)
	try:
		query = builder.query(db.session.query(User), request.args)
	except Exception as e:
		#TODO: maybe return something more meaningful here 
		raise APIException(
                    f"Unable to build query with {request.args}"
                )
	return execute_query(query), 200

@users_blueprint.route('/users', methods=['POST'])
def create_user():
	creator = JSONModelCreator(User)
	try:
		result = creator.create(json.loads(request.data))
		db.session.add(result)
		db.session.commit()
	except Exception as e:
		#TODO: catch sqlalchemy.exc.IntegrityError to see if its a duplicate entry 
		raise e

	return f"{result} - {result.id}", 201


@users_blueprint.route('/api/health', methods=['GET'])
def health():

	return "I'm up! :)", 201


