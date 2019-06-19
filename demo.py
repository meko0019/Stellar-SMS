import requests

from client.database import db
from tests.client.factories import create_sms, UserFactory, AddressFactory

def populate_db(db):
    """
	Creates: - User Alice
			 - Address with username Bob and a stellar address 
	"""
    user = UserFactory()
    user.username = "Alice"
    address = AddressFactory()
    address.username = "Bob"
    address.user = user
    db.session.add(user)
    db.session.add(address)
    db.session.commit()
    return user, address


def send_payment(data):
    alice, bob = populate_db()
    data = create_sms(data).to_dict()
    r = requests.post("http://localhost:8000/api/messages/sms", data=data)

    # assert False