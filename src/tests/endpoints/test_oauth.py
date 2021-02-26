from src.core.config import BASE_PATH_API


def test_obtain_token_api(test_client, test_user_data, test_user_object_data):
    response = test_client.post(f'{BASE_PATH_API}/oauth/token', data={
        'grant_type': 'password',
        'username': test_user_data['email'],
        'password': test_user_data['password'],
    })

    assert response.status_code == 200
    assert response.json()['access_token']
    assert response.json()['token_type'] == 'bearer'


def test_obtain_token_info_api(test_client, access_token):
    response = test_client.get(f'{BASE_PATH_API}/oauth/tokeninfo?token={access_token}')
    assert response.status_code == 200


def test_obtain_token_info_api_failed(test_client):
    response = test_client.get(f'{BASE_PATH_API}/oauth/tokeninfo?token=wrongtoken')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Token is not valid'