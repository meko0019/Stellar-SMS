import os

import redis
from stellar_base.builder import Builder

from client.users.models import User
from client.users import UserDoesNotExistError
from config import REDIS_URL


def tx_pending(phone_num, conn=None):
    if conn is None:
        conn = redis.Redis.from_url(REDIS_URL)
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
