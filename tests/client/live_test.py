import requests
import time

import redis
from flask import current_app

from client.database import db
from client.database.utils import delete_all_rows
from client.factory import celery
from client.stellar.utils import create_account
from tests.client.factories import create_sms, UserFactory, AddressFactory
from config import REDIS_URL


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
    delete_all_rows(current_app)
    conn = redis.Redis.from_url(REDIS_URL)
    conn.flushall()
    celery.conf.update({"task_always_eager": True})
    alice, bob = populate_db()
    data = create_sms(msg).to_dict()
    data["From"] = alice.phone_number
    alice_kp = create_account(alice)
    bob_kp = create_account(bob)
    r = requests.post("http://web:8000/api/messages/sms", data=data)
    time.sleep(10)  # wait until tx is processed
    assert r.status_code == 200

    data = create_sms("yes").to_dict()
    data["From"] = alice.phone_number
    r = requests.post("http://web:8000/api/messages/sms", data=data)
    assert r.status_code == 200


if __name__ == "__main__":
    live()
