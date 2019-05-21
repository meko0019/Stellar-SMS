import json
from flask import request, Blueprint

from client.database import db
from client.messages.models import Message

msgs_blueprint = Blueprint('messages', __name__, url_prefix='/api/messages')

@msgs_blueprint.route('/', methods=['POST'])
def create_msg():
	message = json.loads(request.data)
	db.session.add(message)
	db.session.commit()
	return str(message.__json__())




