import pytest
from app import app
from models.damage_state import DamageState

@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route."""
    response = client.get('/')
    s = DamageState.APPROVED
    assert response.status_code == 201