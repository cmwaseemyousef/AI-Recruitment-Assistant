# AI Recruitment Assistant

A Flask-based API that uses OpenAI's GPT to analyze resumes.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your OpenAI API key
5. Run the application:
   ```bash
   python app/main.py
   ```

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /analyze-resume`: Analyze a resume
  - Request body: `{"resume": "resume text"}`
  - Response: `{"analysis": "analysis result"}`

## Testing

Run tests with:
```bash
pytest
```

## 📜 License
This project is licensed under the MIT License.

# ✅ File Placement Guide:
- `LICENSE`: Place in the **root directory** of your project (same level as README.md).
- `.gitignore`: Place in the **root directory**.
- `requirements.txt`: Place in the **root directory**.
- `README.md`: Place in the **root directory**.
- `app.py`, `__init__.py`: Place inside the `app/` directory.

Your project is now **Portfolio-Ready! 🚀✨**