from google import genai
from dotenv import load_dotenv
from app.config.config import get_settings


load_dotenv()

settings = get_settings()
genai_client = genai.Client(api_key=settings.gemini_api_key)
