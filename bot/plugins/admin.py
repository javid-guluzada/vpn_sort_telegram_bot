from pyrogram import Client, filters
from pyrogram.types import Message
from bot import ADMINS, OWNER_ID
from bot.utils.helpers.authorize import authorize_admin
from bot.utils.database.database import db
import logging


@Client.on_message(filters.command("log"))
async def log(c: Client, m: Message):
    if not authorize_admin(m.from_user.id):
        return
    await m.reply_document("log.txt")


# add_admin
@Client.on_message(filters.command("add_admin"))
async def add_admin(c: Client, m: Message):
    if not authorize_admin(m.from_user.id):
        return
    if m.reply_to_message:

        user_id = m.reply_to_message.from_user.id
    else:
        try:
            _, user_id = m.text.split(" ", 1)
            user_id = int(user_id)
        except:
            return await m.reply_text("Reply to a message or provide a user id")
    if user_id == OWNER_ID:
        return await m.reply_text("He is the owner of the bot, duh!")

    if user_id in ADMINS:
        return await m.reply_text("User is already an admin")
    ADMINS.add(user_id)
    db.add_admin(user_id)
    await m.reply_text("Admin added")


# remove_admin
@Client.on_message(filters.command("remove_admin"))
async def remove_admin(c: Client, m: Message):
    if not authorize_admin(m.from_user.id):
        return
    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        try:
            _, user_id = m.text.split(" ", 1)
            user_id = int(user_id)
        except:
            return await m.reply_text("Reply to a message or provide a user id")

    if user_id == OWNER_ID:
        return await m.reply_text("He is the owner of the bot, duh!")

    if user_id not in ADMINS:
        return await m.reply_text("User is not an admin")
    ADMINS.remove(user_id)
    db.remove_admin(user_id)
    await m.reply_text("Admin removed")


# get_admins
@Client.on_message(filters.command("admins"))
async def get_admins(c: Client, m: Message):
    if not authorize_admin(m.from_user.id):
        return
    admins = db.get_admins()
    msg = "\n".join([f"{admin[0]}" for admin in admins])
    await m.reply_text(f"Admins:\n{msg}")
