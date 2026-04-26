import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_add_page_loads(client):
    """Add recipe page returns 200."""
    response = client.get("/add")
    assert response.status_code == 200


def test_app_exists():
    """App is created successfully."""
    assert app is not None


def test_testing_config(client):
    """Testing config is set correctly."""
    assert app.config["TESTING"] is True
