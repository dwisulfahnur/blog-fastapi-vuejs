import pytest
from starlette.config import environ
from starlette.testclient import TestClient
from datetime import timedelta
environ["TESTING"] = "TRUE"


@pytest.fixture(scope="session")
def test_user_data():
    return {
        "email": "user1@example.com",
        "full_name": "string test1",
        "password": "string1-min8",
    }


@pytest.fixture(scope='session')
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    return loop


@pytest.fixture(scope="session")
def test_user_object_data(event_loop, test_user_data):
    from src.models.user import User
    user = event_loop.run_until_complete(User.get_by_email(test_user_data['email']))
    if not user:
        user = event_loop.run_until_complete(
            User.register_new_user(
                email=test_user_data['email'],
                full_name=test_user_data['full_name'],
                password=test_user_data['password'],
            ))
    return user


@pytest.fixture(scope="session")
def access_token(test_user_object_data):
    return test_user_object_data.create_access_token(timedelta(hours=1))


@pytest.fixture(scope="session")
def test_client(event_loop):
    from src.main import app
    from src.core.config import database_name
    with TestClient(app) as test_client:
        yield test_client
        app.dependency_overrides = {}

    # Delete database testing after test already finished
    from src.core.db import get_client
    client = get_client()
    client.drop_database(database_name)
