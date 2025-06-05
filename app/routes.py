from flask import Blueprint, jsonify, request
from .services import analyze_resume
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
import io

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Recruitment Assistant!"})

@main_routes.route('/health')
def health_check():
    return jsonify({"status": "up and running"})

@main_routes.route('/analyze-resume', methods=['POST'])
def analyze():
    data = request.json
    resume_text = data.get("resume", "")
    if not resume_text:
        return {"error": "No resume text provided"}, 400
    result = analyze_resume(resume_text)
    return result

@main_routes.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.pdf'):
        try:
            pdf_reader = PdfReader(io.BytesIO(file.read()))
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()

            if not text.strip():
                return jsonify({"error": "Could not extract text from PDF. The PDF might be empty or scanned (e.g. image-based)."}), 400

            result = analyze_resume(text)
            return jsonify(result)
        except PdfReadError:
            return jsonify({"error": "Could not read PDF. File may be corrupted, password-protected, or not a valid PDF."}), 422  # Unprocessable Entity
        except Exception as e:
            # General error catch for other unexpected issues
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Please upload a PDF file."}), 415 # Unsupported Media Type
