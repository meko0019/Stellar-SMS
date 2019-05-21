from client.celery import celery


@celery.task
def send_payment(tx):
	pass


def process_tx():
	pass