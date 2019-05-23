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
def add(x,y):
	return x+y