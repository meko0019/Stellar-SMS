import os

import redis

from client.database import db
from client.factory import celery
from client.log import c_logger as log
from client.transactions.utils import otp_required, acquire_lock, release_lock
from client.transactions.models import Payment
from client.stellar.utils import send_payment
from client.users.models import User
from config import REDIS_URL


@celery.task
def process_tx(from_):
    log.debug("Processing transaction.. ")
    conn = redis.Redis.from_url(REDIS_URL)
    tx_key = "tx:" + from_
    tx = conn.hgetall(tx_key)
    user = User.query.filter_by(phone_number=tx.get(b"from").decode("utf-8")).first()
    sender_seed = user.keypair_seed
    log.debug("Transaction is ready for submission.")
    #lock tx to ensure only 1 worker is working on the tx at a given time
    #and watch for any changes made to the tx by a different process during submission 
    lock = acquire_lock(conn, tx_key)
    pipe = conn.pipeline(True)
    pipe.watch(tx)
    if send_payment(sender_seed, tx):
        pipe.multi()
        pipe.delete(tx_key)
        pipe.execute()
    else:
        pipe.unwatch()
    release_lock(conn, tx_key, lock)


@celery.task
def create_tx(from_, to, amount, currency, action="send"):
    log.debug("Creating transaction.. ")
    user = User.query.filter_by(phone_number=from_).first()
    if user is None:
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
    payment = Payment(
        destination=tx["to"],
        amount=tx["amount"],
        asset=tx["currency"],
        fee="100",
        sender=user,
    )
    db.session.add(payment)
    db.session.commit()
    log.debug(f"Created transaction with key {tx_key} and tx {tx}.")

    return tx_summary(from_, to, amount, currency)


def tx_summary(from_, to, amount, currency="XLM"):
    reply = "your one time password" if otp_required(from_) else "Y or Yes"
    return "Here's your transaction summary: \nAmount: {} \nTo: {} {}. \nPlease reply with {}".format(
        amount, to, currency, reply
    )
    # TODO: reply via sms
