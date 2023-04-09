import os

from dotenv import load_dotenv

load_dotenv()


REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")