from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from client.database import db, BaseModel, UTCNOW, isofmt_date


class Message(BaseModel):
	__tablename__ = 'messages'

	msg_id = db.Column(db.String(64), index=True, nullable=False, unique=True)
	body = db.Column(db.String(128), index=True)
	user_id = db.Column(db.Integer, ForeignKey('users.id'))
	sender = relationship('User')
	unread = db.Column(db.Boolean(), server_default='true')
	time_created = db.Column(db.Date(), server_default=UTCNOW(), index=True)
	recieved_at = db.Column(db.Date(), index=True)

	def __repr__(self):
	    return '<Message {}>'.format(self.msg_id) 

	def __json__(self):
		json = super().__json__()
		json.update({'message id': self.msg_id,
					'body': self.body,
					'from': self.sender.phone_number,
					'recieved_at': isofmt_date(self.recieved_at),

			})
		return json

