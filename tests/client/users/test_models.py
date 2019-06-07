from client.users.models import User, Address
from tests.client.factories import UserFactory, AddressFactory


def test_create_user(db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()

    query = db_session.query(User).filter(User.first_name == user.first_name).all()
    len(query) == 1
    assert query[0] == user


def test_password_hash(db_session):
    user = UserFactory()
    user.set_password("Thisisatestpassword!")
    db_session.add(user)
    db_session.commit()
    query = db_session.query(User).all()
    assert user == query[0]

    user = query[0]
    assert user.password_hash != "Thisisatestpassword!"
    assert user.check_password("Thisisatestpassword!")


def test_create_address(db_session):
    user = UserFactory()
    address = AddressFactory()
    address.user = user
    db_session.add(user)
    db_session.add(address)
    db_session.commit()

    query = db_session.query(User).all()
    len(query) == 1
    assert user == query[0]

    query = db_session.query(Address).all()
    len(query) == 1
    assert address == query[0]

    address = query[0]
    assert address.user == user
