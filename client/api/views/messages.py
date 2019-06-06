import json
from flask import request, Blueprint

from client.log import c_logger as log
from client.database import db
from client.messages.models import Message
from client.messages.utils import sms_handler

from twilio.twiml.messaging_response import MessagingResponse

msgs_blueprint = Blueprint("messages", __name__, url_prefix="/api/messages")


@msgs_blueprint.route("/sms", methods=["GET", "POST"])
def incoming_sms():
    try:
        message = request.values.to_dict()
        log.debug(message)
        resp_body = sms_handler(request.values)
    except Exception as e:
        log.error(e)
        return str(MessagingResponse())
    resp = MessagingResponse()
    resp.message(resp_body)
    return str(resp)


@msgs_blueprint.route("/", methods=["POST"])
def create_msg():
    message = json.loads(request.data)
    db.session.add(message)
    db.session.commit()
    return str(message.__json__())
