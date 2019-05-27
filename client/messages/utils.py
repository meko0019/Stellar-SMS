import re 

from client.transactions.tasks import process_tx, create_tx

SEND_PATTERN = re.compile(r'^(send)(\s*\w+)(\s*\d+)(\s*\w*)$')

def sms_handler(message):
	body = message.get('body').strip().lower()
	from_ = message.get('from')
	if tx_pending(from_):
		if body in ['y', 'yes']:
			otp = otp_required(from_)
			if otp:
				return 'Please reply with your one time password.'
			process_tx.delay(from_)
			return 'Your transaction has been submitted.'
		if check_otp(from_, body):
			process_tx.delay(from_)
			return 'Your transaction has been submitted.'
		return "Your transaction has been canceled"

	sms_parser(from_, body, otp)


def sms_parser(from_, sms, otp):
	match = SEND_PATTERN.match(sms)
	if not match:
		return 'Invalid transaction. Please try again.'
	if len(match.group(2)) == 56: #stellar address (public key)
		create_tx.delay(from_, *match.groups())
		return tx_summary(*match.groups())
	return 'Invalid address. Please try again.'
	#TODO: handle federation addresses

def check_otp(phone_num, msg):
	pass


def otp_required(phone_num):
	pass

def tx_summary(to, amount, currency='XLM', otp=False):
	reply = 'your one time password' if otp else 'Y or Yes'
	return "Here's your transaction summary: \n Amount: {} \n To: {} {}. \n {}.".format(amount, to, currency, reply)


