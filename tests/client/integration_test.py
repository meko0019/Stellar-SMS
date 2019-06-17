import time

from flask import url_for

from client.factory import celery
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
    celery.conf.update({"task_always_eager": True})
    conn.flushall()  # flush redis db
    alice, bob = populate_db(db_session)
    from_, to = alice.phone_number, bob.address
    data = create_sms("send bob 10").to_dict()
    data["From"] = from_
    res = client.post(url_for("messages.incoming_sms"), data=data)
    assert res.status_code == 200
    # wait for tasks to finish
    time.sleep(0.5)
    db_session.merge(alice, bob)
    assert {
        key.decode("utf-8"): val.decode("utf-8")
        for key, val in conn.hgetall("tx:" + alice.phone_number).items()
    }.items() == {"from": from_, "to": to, "amount": "10", "currency": "XLM"}.items()
