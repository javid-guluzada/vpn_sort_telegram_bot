from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.helpers.authorize import authorize_admin

HELP_TEXT = """
I'm a bot that sorts vpn servers based on country and speed

type /get_vpns to get started
"""

ADMIN_HELP_TEXT = """
/add_admin - Add an admin to the bot
/remove_admin - Remove an admin from the bot
/admins - Get a list of admins
/log - Get the log file
"""


@Client.on_message(filters.command("start"))
async def start(c: Client, m: Message):
    await m.reply_text(f"Hi {m.from_user.mention}, I'm vpn sort bot")


@Client.on_message(filters.command("help"))
async def help(c: Client, m: Message):
    if not authorize_admin(m.from_user.id):
        return await m.reply_text(HELP_TEXT)
    await m.reply_text(HELP_TEXT + ADMIN_HELP_TEXT)
