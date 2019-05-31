import random

import pytest
import factory
from client.messages.utils import sms_handler, sms_parser

import client
from tests.client.factories import (
    create_sms,
    generate_otp,
    generate_stellar_address as gsa,
)


@pytest.mark.parametrize(
    "sms_body,expected",
    [
        ("send " + gsa() + " 10", ""),
        ("send " + gsa() + " 10 xlm", ""),
        ("send " + gsa() + " 10usd", ""),
        ("send " + gsa()[1:] + " 10", "Invalid address. Please try again."),
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
    assert sms_parser(factory.Faker("phone_number").generate(), sms_body) == expected


def test_sms_handler_pending_tx(mocker):
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


def test_sms_handler_new_tx(mocker):
    mocker.patch("client.messages.utils.tx_pending", lambda phone_number: None)
    mocker.patch("client.messages.utils.sms_parser")
    message = create_sms(("send " + gsa() + " 10 xlm"))
    sms_handler(message)
    body = message.get("Body").strip().lower()
    from_ = message.get("From")
    client.messages.utils.sms_parser.assert_called_once_with(from_, body)
