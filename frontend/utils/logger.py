"""Logging configuration for Streamlit frontend"""
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Log file with timestamp
LOG_FILE = os.path.join(LOGS_DIR, "voice_tutor.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Get logger
logger = logging.getLogger("voice_tutor")
