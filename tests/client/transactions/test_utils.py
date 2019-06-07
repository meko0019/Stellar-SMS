import random
import string

from client.transactions.utils import tx_pending, check_otp, otp_required
from tests.client.factories import UserFactory, create_tx


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
