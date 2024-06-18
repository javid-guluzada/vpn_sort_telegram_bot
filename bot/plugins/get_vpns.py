from pyrogram import Client, filters
from pyrogram.types import Message
from bot import VPN_TYPES
from bot.utils.helpers.vpns import get_servers
from bot.utils.helpers.formatters import speed_format_reverse, format_vpn_name
from bot.utils.helpers.flags import get_flag
import logging

log = logging.getLogger(__name__)


@Client.on_message(filters.command("get_vpns"))
async def get_vpns(c: Client, m: Message):
    msg = "\n".join(
        [
            f"{vpn['id']}. {vpn['name']} - /get_countries_{vpn['id']}"
            for vpn in VPN_TYPES
        ]
    )
    await m.reply_text(msg)


@Client.on_message(filters.regex("^/get_countries"))
async def get_countries(c: Client, m: Message):
    text = m.text.replace("@testbot12673_bot", "").strip()
    try:
        _, _, vpn_id = text.split("_")
    except ValueError:
        return await m.reply_text("Invalid command format")
    vpn_id = int(vpn_id)
    if vpn_id > len(VPN_TYPES) or vpn_id < 1:
        return await m.reply_text("Invalid vpn id")
    msg = "\n".join(
        [
            f"{country['id']}. {get_flag(format_vpn_name(country['name']))} {country['name']} - /get_{vpn_id}_{country['id']}"
            for country in VPN_TYPES[vpn_id - 1]["countries"]
        ]
    )
    await m.reply_text(msg)


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
        (
            country
            for country in VPN_TYPES[vpn_id - 1]["countries"]
            if country["id"] == country_id
        ),
        None,
    )
    if not country:
        return await m.reply_text("Invalid country id")

    message = await m.reply_text(f"Fetching servers for {country['name']}...")

    log.info(f"Fetching servers for {country['name']}...")

    servers = await get_servers(country["url"])
    msg = ""
    for i, server in enumerate(servers):
        isAviable = "Yes" if server["aviable"] == "Available" else "No"
        speed_text = speed_format_reverse(server["speed"])
        msg += f"{i+1}. <a href='{server['link']}'>{server['name']}</a>\n<b>Speed</b> - {speed_text}\n<b>Active days</b> - {server['activeDays']} | <b>Aviable:</b> - {isAviable}\n\n"

    await message.edit(
        msg,
        disable_web_page_preview=True,
    )
