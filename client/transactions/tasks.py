import os

import redis
from client.factory import celery
from client.transactions.utils import otp_required
from client.transactions.models import Payment
from client.stellar.utils import send_payment
from config import REDIS_URL


@celery.task
def process_tx(phone_number):
    conn = redis.Redis.from_url(REDIS_URL)
    tx_key = "tx:" + from_
    tx = conn.hgetall(tx_key)
    user = User.query.filter_by(phone_number=tx.get("from")).first()
    sender_seed = user.keypair_seed
    send_payment(sender_seed, tx)


@celery.task
def create_tx(from_, to, amount, currency, action="send"):
    if currency is None:
        currency = "XLM"
    conn = redis.Redis.from_url(REDIS_URL)
    tx_key = "tx:" + from_
    tx = {"from": from_, "to": to, "amount": amount, "currency": currency}
    conn.hmset(tx_key, tx)
    tx_summary(from_, to, amount, currency)


def tx_summary(from_, to, amount, currency="XLM"):
    reply = "your one time password" if otp_required(from_) else "Y or Yes"
    return "Here's your transaction summary: \nAmount: {} \nTo: {} {}. \nPlease reply with {}".format(
        amount, to, currency, reply
    )
    # TODO: send sms
