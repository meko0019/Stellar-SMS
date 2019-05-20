import json
from flask import request, Blueprint

from client.users.models import User
from client.database import db

users_blueprint = Blueprint('users', __name__, url_prefix="/api/users")

@users_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
    	result = User.query.get(user_id).__json__()
    except AttributeError as e:
    	return f"Error: User with id {user_id} does not exist.", 404
    return str(result), 200

@users_blueprint.route('/', methods=['GET'])
def get_users():
	try:
		query = User.query.all()
	except Exception as e:
		#TODO: maybe return something more meaningful here 
		raise e
	return list(query), 200

@users_blueprint.route('/', methods=['POST'])
def create_user():
	user = User(**json.loads(request.data))
	db.session.add(user)
	db.session.commit()

	return f"{user.__json__()}", 201


