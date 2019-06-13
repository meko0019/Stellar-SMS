import os

import redis

from client.factory import celery
from client.log import c_logger as log
from client.transactions.utils import otp_required
from client.transactions.models import Payment
from client.stellar.utils import send_payment
from client.users.models import User
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
    log.debug("Creating transaction.")
    if User.query.filter_by(phone_number=from_).first() is None:
        log.error("User does not exist.")
        return
    if currency is None or currency == "":
        currency = "XLM"
    conn = redis.Redis.from_url(REDIS_URL)
    tx_key = "tx:" + from_
    tx = {
        "from": from_.strip(),
        "to": to.strip(),
        "amount": amount.strip(),
        "currency": currency.strip(),
    }
    conn.hmset(tx_key, tx)
    log.debug(f"Created transaction with key {tx_key} and tx {tx}.")
    tx_summary(from_, to, amount, currency)


def tx_summary(from_, to, amount, currency="XLM"):
    pass
    # reply = "your one time password" if otp_required(from_) else "Y or Yes"
    # return "Here's your transaction summary: \nAmount: {} \nTo: {} {}. \nPlease reply with {}".format(
    #     amount, to, currency, reply
    # )
    # TODO: send sms
