import time

import requests
from flask import url_for

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
    db.add(user)
    db.add(address)
    db.commit()
    return user, address


def test_integration(client, db_session, conn):
    conn.flushall()  # flush redis db
    alice, bob = populate_db(db_session)
    data = create_sms("send bob 10").to_dict()
    data['From'] = alice.phone_number
    res = client.post(url_for("messages.incoming_sms"), data=data)
    assert res.status_code == 200
    #wait for tasks to finish
    time.sleep(0.5)
    assert {key.decode('utf-8'):val.decode('utf-8') for key, val in conn.hgetall("tx:" + alice.phone_number).items()}.items() == {
        "from": alice.phone_number,
        "to": bob.address,
        "amount": "10",
        "currency": "XLM",
    }.items()
