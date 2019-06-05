from tests.client.factories import UserFactory, create_tx
from client.transactions.utils import tx_pending


def test_tx_pending(conn):
    conn.flushall()
    tx_key, tx = create_tx()
    assert tx_pending(tx.get("from"), conn) == False
    conn.hmset(tx_key, tx)
    assert tx_pending(tx.get("from"), conn)
