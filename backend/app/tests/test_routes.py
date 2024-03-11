import pytest
import os
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_dir)
from app import create_app  # Adjust the import path to match your project structure


@pytest.fixture
def app():
    # Load the application with test configuration
    test_app = create_app()
    
   
    yield test_app

@pytest.fixture
def client(app):
    # This fixture provides a test client for the app
    with app.test_client() as client:
        yield client

@pytest.fixture
def runner(app):
    # This fixture provides a CLI runner for the app
    return app.test_cli_runner()

def test_login(client):
    # Example test for the login endpoint
    response = client.post('/api/login', json={
        'email': 'test@gmail.com',
        'password': 'test',
    })
    assert response.status_code == 200

def test_recipe_info(client):
    # Use the test_recipe_data fixture to get the recipe_id
    recipe_id = "f2090ba4-eb6c-448e-bf8f-3436118c6c32"
    response = client.get(f'/api/recipe_info?recipe_id={recipe_id}')
    assert response.status_code == 200
    data = response.json
    assert data['recipe_id'] == recipe_id
    assert data['name'] == "Pepperoni pizza"


def test_user_info(client):
    # Use the test_recipe_data fixture to get the recipe_id
    user_id = "df49b57e-a65f-416b-944c-41f88203f9d3"
    response = client.get(f'/api/user_info?user_id={user_id}')
    assert response.status_code == 200
    data = response.json
    assert data['username'] == "test"
    

