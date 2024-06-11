from pyrogram import Client, filters, enums
from pyrogram.types import Message
from bot import COUNTRIES
from bot.utils.helpers.vpns import get_servers


@Client.on_message(filters.command("get_countries"))
async def get_countries(c: Client, m: Message):
    countries = "\n".join(
        [f"{i+1}. /get_{country['name']}" for i, country in enumerate(COUNTRIES)]
    )
    await m.reply_text(countries)


# custom filter to check if the command starts with "get_"
@Client.on_message(filters.regex(r"^/get_"))
async def get_servers_s(c: Client, m: Message):
    country_name = m.text.replace("/get_", "").replace("@testbot12673_bot", "").strip()
    message = await m.reply_text(f"Fetching servers for {country_name}...")
    # get the country link from the list of COUNTRIES where the name matches the country
    country_url = next(
        (country["url"] for country in COUNTRIES if country["name"] == country_name),
        None,
    )

    print(country_url)
    servers = get_servers(country_url)
    new_message_text = ""
    for i, server in enumerate(servers):
        # add the server name with hyperlink to the message and speed
        new_message_text += (
            f"{i+1}. [{server['name']}]({server['link']}) - {server['speed']} Mbit/s\n"
        )
    await message.edit(
        new_message_text,
        parse_mode=enums.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
