from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger
from os import getenv, remove, path

from dotenv import load_dotenv
from bot.utils.helpers.vpns import get_vpn_types
from bot.utils.database.database import db


if path.exists("log.txt"):
    remove("log.txt")

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

BOT_USERNAME = ""

ADMINS = set()
if getenv("ADMINS"):
    for admin in getenv("ADMINS").split(" "):
        ADMINS.add(int(admin))

for admin in db.get_admins():
    ADMINS.add(admin[0])


VPN_TYPES = get_vpn_types()
