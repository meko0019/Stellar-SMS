from client.users.models import User
from tests.client.factories import UserFactory


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
