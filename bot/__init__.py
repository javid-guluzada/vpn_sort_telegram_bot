import json
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger
from os import getenv, remove

from dotenv import load_dotenv
from bot.utils.helpers.vpns import get_countries


# remove("log.txt")

basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[FileHandler("log.txt"), StreamHandler()],
    level=INFO,
)

LOGGER = getLogger("Vpn Sort Bot")
load_dotenv("config.env", override=True)
try:
    API_ID = int(getenv("API_ID"))
except:
    API_ID = None
API_HASH = getenv("API_HASH")
if not API_HASH.strip():
    API_HASH = None
BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN.strip():
    BOT_TOKEN = None
try:
    OWNER_ID = int(getenv("OWNER_ID"))
except:
    OWNER_ID = None
if not all([API_ID, API_HASH, BOT_TOKEN, OWNER_ID]):
    LOGGER.error("One or more env variables missing exiting now!")
    exit(1)


ADMINS = set()
AUTH_CHATS = set()

admins = getenv("ADMINS")
auth_chats = getenv("AUTH_CHATS")

COUNTRIES = []

countries = get_countries()
for country in countries:
    COUNTRIES.append(country)
