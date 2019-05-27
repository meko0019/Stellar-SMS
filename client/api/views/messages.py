import json
from flask import request, Blueprint

from client.database import db
from client.messages.models import Message
from client.messages.utils import sms_handler

msgs_blueprint = Blueprint('messages', __name__, url_prefix='/api/messages')

@msgs_blueprint.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    resp_body = sms_handler(request.values)
    # Start our TwiML response
    resp = MessagingResponse()

    resp.message(resp_body)

    return str(resp)

@msgs_blueprint.route('/', methods=['POST'])
def create_msg():
	message = json.loads(request.data)
	db.session.add(message)
	db.session.commit()
	return str(message.__json__())




