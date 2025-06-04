from flask import Blueprint, jsonify, request
from .services import analyze_resume

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Recruitment Assistant!"})

@main_routes.route('/health')
def health_check():
    return jsonify({"status": "up and running"})

@main_routes.route('/analyze-resume', methods=['POST'])
def analyze():
    """Analyze the provided resume text."""
    # Safely parse JSON, falling back to an empty dict if parsing fails
    data = request.get_json(silent=True) or {}
    resume_text = data.get("resume", "")

    if not resume_text:
        return {"error": "No resume text provided"}, 400

    result = analyze_resume(resume_text)
    return result
