import random
import string
import time

import redis

from client.transactions.utils import (
    tx_pending,
    check_otp,
    otp_required,
    acquire_lock,
    release_lock,
)
from tests.client.factories import UserFactory, create_tx
from config import REDIS_URL


def test_tx_pending(conn):
    conn.flushall()
    tx_key, tx = create_tx()
    assert tx_pending(tx.get("from"), conn) == False
    conn.hmset(tx_key, tx)
    assert tx_pending(tx.get("from"), conn)


def test_check_otp(db_session):
    user = UserFactory()
    one_time_password = "".join(
        random.choices(string.ascii_letters + string.digits, k=8)
    )
    user.set_password(one_time_password)
    db_session.add(user)
    db_session.commit()
    assert check_otp(user.phone_number, one_time_password)


def test_otp_required(db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    assert otp_required(user.phone_number) == False


def test_acquire_and_release_lock():
    conn = redis.Redis.from_url(REDIS_URL)
    lock = acquire_lock(conn, "testlock123", lock_timeout=2)
    new_conn = redis.Redis.from_url(REDIS_URL)
    assert (
        acquire_lock(new_conn, "testlock123", acquire_timeout=1, lock_timeout=2)
        == False
    )

    time.sleep(2)
    lock = acquire_lock(new_conn, "testlock123", lock_timeout=2)
    assert lock

    assert acquire_lock(conn, "testlock123", acquire_timeout=1, lock_timeout=2) == False
    assert release_lock(new_conn, "testlock123", lock)
    assert acquire_lock(conn, "testlock123", lock_timeout=2)
