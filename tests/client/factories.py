import datetime
import random
import string
from pytz import UTC

from werkzeug.datastructures import CombinedMultiDict, ImmutableMultiDict

import factory.fuzzy

from client.messages.models import Message
from client.users.models import User


class BaseModelFactory(factory.Factory):
    class Meta:
        abstract = True


class MessageFactory(BaseModelFactory):
    class Meta:
        model = Message

    msg_id = factory.fuzzy.FuzzyText(length=64)
    body = factory.fuzzy.FuzzyText(length=128)
    recieved_at = factory.fuzzy.FuzzyDateTime(datetime.datetime(2018, 1, 1, tzinfo=UTC))


class UserFactory(BaseModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user%d" % n)
    email_address = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Faker("phone_number")


def create_sms(body):
    msg_obj = CombinedMultiDict(
        [
            ImmutableMultiDict([]),
            ImmutableMultiDict(
                [
                    ("ToCountry", "US"),
                    ("ToState", "MN"),
                    (
                        "SmsMessageSid",
                        "".join(
                            random.choices(string.ascii_letters + string.digits, k=34)
                        ),
                    ),
                    ("NumMedia", "0"),
                    ("ToCity", "MINNEAPOLIS"),
                    ("FromZip", factory.Faker("zipcode").generate()),
                    (
                        "SmsSid",
                        "".join(
                            random.choices(string.ascii_letters + string.digits, k=34)
                        ),
                    ),
                    ("FromState", "MN"),
                    ("SmsStatus", "received"),
                    ("FromCity", factory.Faker("city").generate()),
                    ("Body", body),
                    ("FromCountry", "US"),
                    ("To", "+16123249990"),
                    (
                        "MessagingServiceSid",
                        "".join(
                            random.choices(string.ascii_letters + string.digits, k=34)
                        ),
                    ),
                    ("ToZip", "55401"),
                    ("NumSegments", "1"),
                    (
                        "MessageSid",
                        "".join(
                            random.choices(string.ascii_letters + string.digits, k=34)
                        ),
                    ),
                    (
                        "AccountSid",
                        "".join(
                            random.choices(string.ascii_letters + string.digits, k=34)
                        ),
                    ),
                    ("From", factory.Faker("phone_number").generate()),
                    ("ApiVersion", "2010-04-01"),
                ]
            ),
        ]
    )
    return msg_obj


def generate_stellar_address():
    return "".join(random.choices(string.ascii_letters + string.digits, k=56))


def generate_otp():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))
