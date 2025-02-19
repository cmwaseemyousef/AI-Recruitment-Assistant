import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'up and running'

def test_analyze_resume_empty(client):
    response = client.post('/analyze-resume', json={})
    assert response.status_code == 400
    assert 'error' in response.json

def test_analyze_resume_with_content(client):
    response = client.post('/analyze-resume', 
                         json={"resume": "Software Engineer with 5 years experience"})
    assert response.status_code == 200
    assert 'analysis' in response.json