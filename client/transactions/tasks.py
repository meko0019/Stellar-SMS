import os

import redis
from client.factory import celery
from client.transactions.utils import otp_required

celery.conf.beat_schedule = {
    "process_tx": {"task": "tasks.process_tx", "schedule": 30.0}
}


@celery.task
def send_payment(tx):
    pass


@celery.task
def process_tx(phone_number):
    pass


@celery.task
def create_tx(from_, to, amount, currency, action="send"):
    if not currency:
        currency = "XLM"
    conn = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6479/0"))
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
