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
OWNER_ID = int(os.environ.get("OWNER_ID", "5296584067"))
TG_WORKERS = int(os.environ.get("BOT_WORKERS", "4"))

PORT = os.environ.get("PORT", "8080")

#start message
START_MSG = os.environ.get("START_MESSAGE", "Hello {first} I'm a bot who can store files and share it via spacial links")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "5296584067").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "You have to join our Channels First")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)
ADMINS.append(5296584067)

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