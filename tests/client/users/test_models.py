from client.users.models import User


def test_basic_search(db_session):
	res = db_session.query(User).filter(User.first_name == "test_user").all()
	assert res == []

	user = User(first_name="test_user", username='test_user')
	db_session.add(user)
	db_session.commit()

	res = db_session.query(User).filter(User.first_name == "test_user").all()
	len(res) == 1
	assert res[0] == user
