import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the AI Recruitment Assistant!"}

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "up and running"}

def test_analyze_resume(client):
    data = {"resume": "John Doe has 5 years of experience in AI."}
    response = client.post("/analyze-resume", json=data)
    assert response.status_code == 200
    assert "resume_analysis" in response.json

def test_analyze_resume_empty(client):
    response = client.post("/analyze-resume", json={})
    assert response.status_code == 400
    assert response.json == {"error": "No resume text provided"}
