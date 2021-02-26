
import pytest

from src.core.config import BASE_PATH_API


@pytest.fixture(scope='module')
def test_post_data():
    return {
        'title': 'Test Post title',
        'content': 'Test content of the post'
    }


@pytest.fixture(scope='module')
def test_create_post(test_client, test_user_object_data, test_post_data, access_token):
    response = test_client.post(f'{BASE_PATH_API}/posts', json=test_post_data, headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 201
    assert response.json()['title'] == test_post_data['title']
    assert response.json()['content'] == test_post_data['content']

def test_create_post_fail(test_client, access_token):
    response = test_client.post(f'{BASE_PATH_API}/posts', headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 422
    assert response.json()

def test_create_post_unauthorized(test_client, test_post_data):
    response = test_client.post(f'{BASE_PATH_API}/posts', json=test_post_data, headers={
        'Authorization': f'Bearer nope'
    })

    assert response.status_code == 401
    assert response.json()

def test_read_post(test_client, test_create_post):
    response = test_client.get(f'{BASE_PATH_API}/posts')

    assert response.status_code == 200
    assert response.json()
