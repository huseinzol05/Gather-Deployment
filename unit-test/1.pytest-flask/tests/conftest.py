import pytest


@pytest.fixture
def client():
    from web import app

    app.config['TESTING'] = True
    yield app.test_client()
