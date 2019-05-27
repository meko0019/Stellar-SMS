import os

import redis
from client.factory import celery

celery.conf.beat_schedule = {
    'process_tx': {
        'task': 'tasks.process_tx',
        'schedule': 30.0,
    },
}

@celery.task
def send_payment(tx):
	pass


def process_tx():
	pass


@celery.task
def create_tx(from_, action, to, amount, currency='XLM'):
	conn = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6479/0"))
	tx_key = "tx:"+from_ 
	tx = {'from': from_, 'to': to, 'amount': amount, 'currency': currency}
	conn.hmset(tx_key, tx)