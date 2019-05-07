from client.users.models import User


def test_create_user(db_session):
	user = User(first_name="test_user", username='test_user')
	db_session.add(user)
	db_session.commit()

	resp = db_session.query(User).filter(User.first_name == "test_user").all()
	len(resp) == 1
	assert resp[0] == user
