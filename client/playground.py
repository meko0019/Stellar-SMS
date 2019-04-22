from stellar_base.keypair import Keypair
import requests

def create_account():
	keypair = Keypair.random()
	publickey = keypair.address().decode()
	seed = keypair.seed().decode()
	url = 'https://friendbot.stellar.org'
	r = requests.get(url, params={'addr': publickey})
	print(f"Public key: {publickey} \nSeed: {seed}")
	return	


def send_money(send_from=None, send_to=None):




def recieve_money():
	pass


