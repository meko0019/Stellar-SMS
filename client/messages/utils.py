import re 

from client.transactions.tasks import process_tx

SEND_PATTERN = re.compile(r'^(send)(\s*\w+)(\s*\d+)(\s*\w*)$')

def msg_parser(message):
	body = message.get('body').strip().lower()
	from_ = message.get('from_')
	if msg == 'y':
		process_tx(from_)
		return 'Your payment has been submitted.'
	match = SEND_PATTERN.match(msg)
	if not match:
		#TODO:
		return 

	if len(match.group(2)) == 56: #stellar address (public key)
		pass 
