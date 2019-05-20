from client.messages.models import Message
from client.users.models import User
from tests.client.factories import MessageFactory, UserFactory

def test_create_message(db_session):
	msg = MessageFactory()
	user = UserFactory()
	msg.sender = user
	db_session.add(msg)
	db_session.commit()

	resp = db_session.query(Message).filter(Message.msg_id == msg.msg_id).all()
	len(resp) == 1
	assert resp[0] == msg

