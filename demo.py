import requests

from tests.client.factories import create_sms


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
    db.add(user)
    db.add(address)
    db.commit()
    return user, address


def send_payment(data):
    alice, bob = populate_db()
    data = create_sms(data).to_dict()
    r = requests.post("http://localhost:8000/api/messages/sms", data=data)
    # assert False
