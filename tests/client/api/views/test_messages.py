import random

from flask import url_for


def test_incoming_sms(client):
    """
	test twilio callback endpoint
	"""
    res = client.get(
        url_for("messages.incoming_sms"),
        data={
            "ToCountry": "US",
            "ToState": "MN",
            "SmsMessageSid": "SMe86aa1c335d373762e171d487df1840f",
            "NumMedia": "0",
            "ToCity": "MINNEAPOLIS",
            "FromZip": "55416",
            "SmsSid": "SMe86aa1c335d373762e171d487df1840f",
            "FromState": "MN",
            "SmsStatus": "received",
            "FromCity": "MINNEAPOLIS",
            "Body": "send alice 10",
            "FromCountry": "US",
            "To": "+16123249990",
            "MessagingServiceSid": "MG35808d2e39da0249b3e51f3c4f427e0c",
            "ToZip": "55401",
            "NumSegments": "1",
            "MessageSid": "SMe86aa1c335d373762e171d487df1840f",
            "AccountSid": "ACcf594d39b60f9c051ec016cc1b321cf8",
            "From": "+19524651324",
            "ApiVersion": "2010-04-01",
        },
    )
    assert res.status_code == 200

    res = client.post(
        url_for("messages.incoming_sms"),
        data={
            "ToCountry": "US",
            "ToState": "MN",
            "SmsMessageSid": "SMe86aa1c335d373762e171d487df1840f",
            "NumMedia": "0",
            "ToCity": "MINNEAPOLIS",
            "FromZip": "55416",
            "SmsSid": "SMe86aa1c335d373762e171d487df1840f",
            "FromState": "MN",
            "SmsStatus": "received",
            "FromCity": "MINNEAPOLIS",
            "Body": "send alice 10",
            "FromCountry": "US",
            "To": "+16123249990",
            "MessagingServiceSid": "MG35808d2e39da0249b3e51f3c4f427e0c",
            "ToZip": "55401",
            "NumSegments": "1",
            "MessageSid": "SMe86aa1c335d373762e171d487df1840f",
            "AccountSid": "ACcf594d39b60f9c051ec016cc1b321cf8",
            "From": "+19524651324",
            "ApiVersion": "2010-04-01",
        },
    )
    assert res.status_code == 200
