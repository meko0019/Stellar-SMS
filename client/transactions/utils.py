import os

import redis

from client.users.models import User
from client.users import UserDoesNotExistError

def tx_pending(phone_num):
    conn = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))
    if conn.exists("tx:" + phone_num):
        return True
    return False


def check_otp(phone_num, msg):
	user = User.query.filter_by(phone_number=phone_num).first()
	if user is None:
		raise UserDoesNotExistError("user does not exists.")
	return user.check_password(msg)


def otp_required(phone_num):
	user = User.query.filter_by(phone_number=phone_num).first()
	if user is None:
		raise UserDoesNotExistError("user does not exists.")
	return user.password_required
