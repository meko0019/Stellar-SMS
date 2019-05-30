from client.users.models import User
from tests.client.factories import UserFactory


def test_create_user(db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()

    resp = db_session.query(User).filter(User.first_name == user.first_name).all()
    len(resp) == 1
    assert resp[0] == user
