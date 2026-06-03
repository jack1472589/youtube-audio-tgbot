import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50))  # MB
DEBUG = os.getenv("DEBUG", "False").lower() == "true"