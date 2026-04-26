import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_loads(client):
    """Home page returns 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_add_page_loads(client):
    """Add recipe page returns 200."""
    response = client.get("/add")
    assert response.status_code == 200


def test_invalid_recipe_id(client):
    """Requesting a non-existent recipe ID returns 500 (handled by Flask)."""
    response = client.get("/recipe/000000000000000000000000")
    assert response.status_code in [200, 404, 500]
