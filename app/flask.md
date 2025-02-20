flask
openai
python-dotenv
```

Then run:
```bash
pip install -r requirements.txt
```

2. **Set Up Environment Variables**: Create a `.env` file in the root directory of your project and add your OpenAI API key.

### [.env](file:///c%3A/Users/user/Desktop/AI-Recruitment-Assistant/.env)

````plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Run the Application**: Start the Flask application by running the `main.py` file.

```bash
python /c:/Users/user/Desktop/AI-Recruitment-Assistant/app/main.py
```

4. **Test the Endpoints**: Use a tool like `curl`, Postman, or your web browser to test the endpoints.

- **Home Endpoint**: 
  ```bash
  curl http://127.0.0.1:5000/
  ```

- **Health Check Endpoint**: 
  ```bash
  curl http://127.0.0.1:5000/health
  ```

- **Analyze Resume Endpoint**: 
  ```bash
  curl -X POST http://127.0.0.1:5000/analyze-resume -H "Content-Type: application/json" -d '{"resume": "Your resume text here"}'
  ```

Ensure that you get appropriate responses from each endpoint. If there are any errors, check the logs for more details.