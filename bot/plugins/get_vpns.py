from pyrogram import Client, filters, enums
from pyrogram.types import Message
from bot import COUNTRIES
from bot.utils.helpers.vpns import get_servers
import logging

log = logging.getLogger(__name__)


@Client.on_message(filters.command("get_countries"))
async def get_countries(c: Client, m: Message):
    countries = "\n".join(
        [
            f"{country['id']}. {country['name']}\n/get_3_{country['id']}"
            for country in COUNTRIES
        ]
    )
    await m.reply_text(countries)


@Client.on_message(filters.regex(r"^/get_"))
async def get_servers_s(c: Client, m: Message):
    text = m.text.replace("@testbot12673_bot", "").strip()
    try:
        _, vpn_id, country_id = text.split("_")
    except ValueError:
        return await m.reply_text("Invalid command format")
    country_id = int(country_id)
    vpn_id = int(vpn_id)  # it will be used later
    country = next(
        (country for country in COUNTRIES if country["id"] == country_id), None
    )
    message = await m.reply_text(f"Fetching servers for {country['name']}...")

    log.info(f"Fetching servers for {country['name']}...")

    servers = await get_servers(country["url"])
    new_message_text = ""
    for i, server in enumerate(servers):
        isAviable = "Yes" if server["aviable"] == "Available" else "No"
        new_message_text += f"{i+1}. [{server['name']}]({server['link']}) - {server['speed']} Mbit/s\nActive days - {server['activeDays']}, Aviable: {isAviable}\n"
    await message.edit(
        new_message_text,
        parse_mode=enums.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
