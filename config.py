import os
import logging 
from logging.handlers import RotatingFileHandler

# API ID'S
API_ID = int(os.environ.get("API_ID", "26254064"))
API_HASH = os.environ.get("API_HASH", "72541d6610ae7730e6135af9423b319c")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8113218662:AAEEZWbD7x3zXnNl-1ofPOa4QNkT3Tngi_k")

# DB
DB_URL = os.environ.get("DB_URL", "mongodb+srv://abidabdullahown7:abidabdullah1425@cluster0.7lgug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "BOT_STATUS")

# CHANNELS ID
UPDATE_CHANNEL = int(os.environ.get("UPDATE_CHANNEL", "-1002355785538"))

# OWNER / SUDO USERS
OWNER = int(os.environ.get("OWNER", "5296584067"))

# Set Up Logger
LOG_FILE_NAME = "botstatus.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)