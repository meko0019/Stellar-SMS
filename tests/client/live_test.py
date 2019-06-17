import requests
import time

from client.database import db
from client.factory import celery
from client.stellar.utils import create_account
from tests.client.factories import create_sms, UserFactory, AddressFactory


def populate_db():
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


def live(msg="send bob 10"):
    celery.conf.update({"task_always_eager": True})
    alice, bob = populate_db()
    data = create_sms(msg).to_dict()
    data["From"] = alice.phone_number
    alice_kp = create_account(alice)
    bob_kp = create_account(bob)
    r = requests.post("http://localhost:8000/api/messages/sms", data=data)
    time.sleep(10)  # wait until tx is processed
    assert r.status_code == 200


if __name__ == "__main__":
    live()
