import os
import uuid
import math
import time

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


def acquire_lock(conn, lockname, acquire_timeout=5, lock_timeout=10):
    identifier = str(uuid.uuid4())  # A 128-bit random identifier.
    lock_timeout = int(math.ceil(lock_timeout))
    end = time.time() + acquire_timeout

    while time.time() < end:
        # Get the lock and set the expiration.
        if conn.setnx(lockname, identifier):
            conn.expire(lockname, lock_timeout)
            return identifier
        elif not conn.ttl(lockname):
            conn.expire(lockname, lock_timeout)

        time.sleep(0.001)

    return False


def release_lock(conn, lockname, identifier):
    pipe = conn.pipeline(True)
    counter = 0

    while True:
        try:
            # watch lock to prevent releasing lock multiple times
            pipe.watch(lockname)
            # Check and verify that we still have the lock.
            if conn.get(lockname).decode("utf-8") == identifier:

                # Release the lock
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True

            pipe.unwatch()
            break

        except redis.exceptions.WatchError:
            pass
        # Someone else did something with the lock (VERY unlikely); retry.
    return False
