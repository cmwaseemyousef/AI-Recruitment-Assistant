import openai
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_resume(resume_text):
    if not openai.api_key:
        logger.error("OpenAI API key not found")
        return {"error": "API key configuration error"}

    try:
        logger.info("Analyzing resume")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant for HR recruitment."},
                {"role": "user", "content": f"Analyze this resume: {resume_text}"}
            ],
            max_tokens=300
        )
        summary = response['choices'][0]['message']['content'].strip()
        logger.info("Resume analysis completed successfully")
        return {"analysis": summary}
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return {"error": "OpenAI API error"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": "Internal server error"}