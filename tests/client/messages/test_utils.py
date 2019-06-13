import random

import pytest
import factory
from client.messages.utils import sms_handler, sms_parser, address_lookup

import client
from tests.client.factories import (
    create_sms,
    generate_otp,
    generate_stellar_address as gsa,
    UserFactory,
    AddressFactory,
)


@pytest.mark.parametrize(
    "sms_body,expected",
    [
        ("send " + gsa() + " 10", ""),
        ("send " + "Bob" + " 10", ""),
        ("send " + gsa() + " 10 xlm", ""),
        ("send " + "Bob" + " 10 xlm", ""),
        ("send " + gsa() + " 10usd", ""),
        ("send " + "Bob" + " 10usd", ""),
        (
            "anythingbutsend " + gsa() + " 10usd ",
            "Invalid transaction. Please try again.",
        ),
    ],
)
def test_sms_parser(sms_body, expected, mocker):
    mocker.patch(
        "client.transactions.tasks.create_tx.delay",
        lambda from_, to, amount, currency: ":)",
    )
    mocker.patch("client.messages.utils.address_lookup", lambda from_, to: ":)")
    assert sms_parser(factory.Faker("phone_number").generate(), sms_body) == expected


def test_sms_handler_pending_tx(db_session, mocker):
    """
	exhaustive test of sms_handler 
	"""
    mocker.patch("client.messages.utils.tx_pending", lambda phone_number: True)
    mocker.patch("client.messages.utils.otp_required", lambda phone_number: True)
    mocker.patch("client.messages.utils.check_otp", lambda phone_number, msg: True)
    mocker.patch("client.transactions.tasks.process_tx.delay")
    message = create_sms(generate_otp())
    assert sms_handler(message) == "Your transaction has been submitted."
    client.transactions.tasks.process_tx.delay.assert_called_with(message.get("From"))

    mocker.patch("client.messages.utils.check_otp", lambda phone_number, msg: False)
    assert sms_handler(message) == "Your transaction has been canceled."

    message = create_sms("yes")
    assert (
        sms_handler(message)
        == "Incorrect password. Your transaction has been canceled."
    )

    mocker.patch("client.messages.utils.otp_required", lambda phone_number: False)
    assert sms_handler(message) == "Your transaction has been submitted."
    client.transactions.tasks.process_tx.delay.assert_called_with(message.get("From"))


def test_sms_handler_new_tx(db_session, mocker):
    mocker.patch("client.messages.utils.tx_pending", lambda phone_number: None)
    mocker.patch("client.messages.utils.sms_parser")
    message = create_sms(("send " + gsa() + " 10 xlm"))
    sms_handler(message)
    body = message.get("Body").strip().lower()
    from_ = message.get("From")
    client.messages.utils.sms_parser.assert_called_once_with(from_, body)


def test_address_lookup(db_session):
    user = UserFactory()
    address = AddressFactory()
    address.user = user

    assert address_lookup(user.phone_number, address.username) is None

    db_session.add(user)
    db_session.add(address)
    db_session.commit()

    assert address_lookup(user.phone_number, address.username) == address.address
