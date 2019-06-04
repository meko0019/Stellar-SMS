from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from client.database import db, BaseModel, UTCNOW, isofmt_date


class Payment(BaseModel):
    __tablename__ = "payments"

    time_created = db.Column(db.Date(), server_default=UTCNOW(), index=True)
    destination = db.Column(db.String(64), index=True, nullable=False)
    amount = db.Column(db.String(16), nullable=False)
    asset = db.Column(db.String(16), index=True)
    fee = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(16), default='pending')
    user_id = db.Column(db.Integer, ForeignKey("users.id"), index=True)
    sender = relationship("User")

    def __repr__(self):
        return "<Payment {} from: {} to: {}>".format(self.id, self.sender.username, self.destination)

    def __json__(self):
        json = super().__json__()
        json.update(
            {
                "time_created id": isofmt_date(self.time_created),
                "destination": self.destination,
                "sender": self.sender.username,
                "amount": self.amount,
                "asset": self.asset,
                "fee": self.fee,
                "status": self.status,
            }
        )
        return json