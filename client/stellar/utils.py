import requests

from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.operation import Payment
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.memo import TextMemo
from stellar_base.horizon import horizon_testnet, horizon_livenet

from client.database import db
from client.users.models import User
from client.stellar import UnknownIssuerError


def create_account(user, kp=None, seed=None):
	if kp is None:
		if seed is None:
			kp = Keypair.random()
		else:
			kp = Keypair.from_seed(seed)
	publickey = kp.address().decode()
	url = 'https://friendbot.stellar.org'
	r = requests.get(url, params={'addr': publickey})
	if r.status_code == 200:
		user.keypair_seed = kp.seed().decode()
		db.session.add(user)
		db.session.commit()
		print('Successfully created an account using Friendbot on the test network')
	else:
		print(r.status_code, r.reason)
	return kp


def send_payment(sender_seed, tx):
	# Generate the sender's Keypair for signing and setting as the source
	sender_kp = Keypair.from_seed(sender_seed)

	# Address for the destination
	destination = tx.get('to')

	# create op
	amount = tx.get('amount')
	if tx.get('currency').upper() == 'XLM':
		asset = Asset('XLM')
	else:
		raise UnknownIssuerError('Unknown currency and/or issuer.')
		#TODO: 
		# Issuer's address
		# ISSUER = tx.get('issuer')	
		# asset = Asset(tx.get('currency').upper(), ISSUER)	

	op = Payment(
	    # Source is also inferred from the transaction source, so it's optional.
	    source=sender_kp.address().decode(),
	    destination=destination,
	    asset=asset,
	    amount=amount
	)

	# create a memo
	msg = TextMemo('Stellar-SMS is dope!!!')

	horizon = horizon_testnet()
	# horizon = horizon_livenet() for LIVENET

	# Get the current sequence of sender
	# Python 3
	sequence = horizon.account(sender_kp.address().decode('utf-8')).get('sequence')
	# Python 2
	# sequence = horizon.account(sender_kp.address()).get('sequence')

	# Construct a transaction
	tx = Transaction(
	    source=sender_kp.address().decode(),
	    sequence=sequence,
	    # time_bounds = {'minTime': 1531000000, 'maxTime': 1531234600},
	    memo=msg,
	    fee=100, # Can specify a fee or use the default by not specifying it
	    operations=[
	        op,
	    ],
	)

	# Build transaction envelope
	envelope = Te(tx=tx, network_id="TESTNET") # or 'PUBLIC'

	# Sign the envelope
	envelope.sign(sender_kp)

	# Submit the transaction to Horizon!
	xdr = envelope.xdr()
	response = horizon.submit(xdr)




