from flask import url_for

from tests.client.factories import create_sms


def test_incoming_sms(client):
    """
	test twilio callback endpoint
	"""
    res = client.get(
        url_for("messages.incoming_sms"), data=create_sms("send alice 10").to_dict()
    )
    assert res.status_code == 200

    res = client.post(
        url_for("messages.incoming_sms"), data=create_sms("send alice 10").to_dict()
    )
    assert res.status_code == 200
