import re

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates, relationship
from sqlalchemy import ForeignKey

from client.database import db, BaseModel, UTCNOW, isofmt_date
from client.messages.models import Message


class Address(BaseModel):
    """
    Address book mapping of stellar addresses to usernames
    """

    __tablename__ = "addresses"
    username = db.Column(db.String(64), index=True, nullable=False)
    address = db.Column(db.String(128), index=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")

    # TODO: add username+user constraint so that usernames are unique in each user's "address space"
    @validates("address")
    def validate_address(self, key, address):
        if not address:
            return

        if len(address) != 56:
            raise AssertionError("Invalid stellar address.")

        return address

    def __repr__(self):
        return "<Alias {}>".format(self.username)

    def __json__(self):
        json = super().__json__()
        json.update(
            {
                "username": self.username,
                "address": self.address,
                "user_link": self.user.username,
            }
        )
        return json


class User(BaseModel):
    __tablename__ = "users"
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email_address = db.Column(db.String(120), index=True, nullable=True, unique=True)
    phone_number = db.Column(db.String(32), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=True)
    joined = db.Column(db.Date(), server_default=UTCNOW(), index=True)
    password_hash = db.Column(db.String(128))
    password_required = db.Column(db.Boolean(), server_default="false")
    keypair_seed = db.Column(db.String(128), server_default="Null")
    addresses = relationship("Address", order_by=Address.id, back_populates="user")
    messages = relationship("Message", order_by=Message.id, back_populates="user")

    @validates("email_address")
    def validate_email(self, key, email):
        if not email:
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("Provided email is not a valid email address")

        return email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates("keypair_seed")
    def validate_keypair(self, key, kp_seed):
        if not kp_seed:
            return
        if self.keypair_seed != "Null":
            raise AssertionError("keypair can only be generated once.")
        return kp_seed

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
