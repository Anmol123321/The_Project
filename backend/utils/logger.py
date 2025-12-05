"""Logging configuration for FastAPI backend"""
import logging
import os

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Log file names
LOG_FILE = os.path.join(LOGS_DIR, "api.log")
ERROR_LOG_FILE = os.path.join(LOGS_DIR, "error.log")

# Configure logging format
LOG_FORMAT = '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'

# Create error logger (separate from root)
error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(ERROR_LOG_FILE)
error_handler.setFormatter(logging.Formatter(LOG_FORMAT))
error_logger.addHandler(error_handler)

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        # Console output
        logging.StreamHandler(),
        # All logs to main file
        logging.FileHandler(LOG_FILE)
    ]
)

def get_logger(name: str):
    """Get a logger instance with the given name"""
    return logging.getLogger(name)

# Main logger
logger = get_logger("backend")
