import os
import shutil
import tempfile

import redis
import pytest

from client import database
from client.database.utils import delete_all_rows
from client.factory import create_app
from config import REDIS_URL


@pytest.yield_fixture(scope="session")
def tmp():
    tmpdir = tempfile.mkdtemp(prefix="pytest-client-", dir="/tmp")
    yield tmpdir
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass


@pytest.fixture(scope="session")
def app(tmp):
    return create_app()


@pytest.fixture(scope="session")
def db(app):
    database.db.app = app
    delete_all_rows(app)
    return database.db


@pytest.fixture(scope="function")
def db_session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function")
def conn():
    conn = redis.Redis.from_url(REDIS_URL)
    yield conn
    conn.flushall()
