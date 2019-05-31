import os

import redis


def tx_pending(phone_num):
    conn = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))
    if conn.exists("tx:" + phone_num):
        return True
    return False


def check_otp(phone_num, msg):
    pass


def otp_required(phone_num):
    pass
