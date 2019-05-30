import re

from sqlalchemy.orm import validates
from client.database import db, BaseModel, UTCNOW, isofmt_date


class User(BaseModel):
    __tablename__ = "users"
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email_address = db.Column(db.String(120), index=True, nullable=True, unique=True)
    phone_number = db.Column(db.String(32), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=True)
    joined = db.Column(db.Date(), server_default=UTCNOW(), index=True)

    @validates("email_address")
    def validate_email(self, key, email):
        if not email:
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("Provided email is not a valid email address")

        return email

    def __repr__(self):
        return "<User {}>".format(self.username)

    def __json__(self):
        json = super().__json__()
        json.update(
            {
                "username": self.username,
                "email_address": self.email_address or "--",
                "first_name": self.first_name,
                "last_name": self.last_name or "--",
                "joined": isofmt_date(self.started_on),
            }
        )
        return json
