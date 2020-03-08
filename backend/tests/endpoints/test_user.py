from backend.core.config import BASE_PATH_API


def test_user_register_api(test_client, test_user_data, test_user_object_data, monkeypatch):
    from backend.models.user import User
    class UserInDBMock(User):
        @classmethod
        async def register_new_user(cls, full_name: str, username: str,
                                    email: str, password: str):
            return test_user_object_data

    monkeypatch.setattr('backend.models.user.User.register_new_user',
                        UserInDBMock.register_new_user)

    response = test_client.post(f'{BASE_PATH_API}/users', json={
        'full_name': test_user_data['full_name'],
        'email': test_user_data['email'],
        'username': test_user_data['username'],
        'password': test_user_data['password'],
    })

    assert response.status_code == 201
    assert response.json()['id']
    assert response.json()['username'] == test_user_data['username']


def test_read_user_me(test_client, test_user_object_data, access_token):
    response = test_client.get(f'{BASE_PATH_API}/users/me', headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 200
    assert response.json()['id'] == str(test_user_object_data.id)
    assert response.json()['username'] == test_user_object_data.username
    assert response.json()['full_name'] == test_user_object_data.full_name
    assert response.json()['email'] == test_user_object_data.email
