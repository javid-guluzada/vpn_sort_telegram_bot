from pyrogram import Client, __version__, enums
from pyrogram.raw.all import layer

from bot import API_HASH, API_ID, BOT_TOKEN, LOGGER, BOT_USERNAME


class Bot(Client):
    def __init__(self):
        name = "bot"
        super().__init__(
            name,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root=f"{name}/plugins"),
            parse_mode=enums.ParseMode.HTML,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        BOT_USERNAME = me.username
        LOGGER.info(
            f"@{BOT_USERNAME}  started. Pyrogram v{__version__} (Layer {layer})"
        )

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("Bot stopped. Bye.")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
