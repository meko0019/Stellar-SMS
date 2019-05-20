import datetime
from pytz import UTC

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

    username = factory.Faker('username')
    email_address = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = factory.Faker('phone_number')

