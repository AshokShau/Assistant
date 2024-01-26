import logging
from time import time

from pyrogram import Client, enums

import config

StartTime = time()

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)
SUDO_USERS = config.SUDO_USER


class App(Client):
    def __init__(self):
        super().__init__(
            name="Assistant",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            lang_code="en",
            bot_token=config.TOKEN,
            plugins=dict(root="Assistant.modules"),
            in_memory=True,
            parse_mode=enums.ParseMode.DEFAULT,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention
        try:
            await self.send_message(config.LOGGER_ID, "<b>Bot Started</b>")
        except:
            LOGGER.error(
                "Bot has failed to access the log group. Make sure that you have added your bot to your log group."
            )
            exit()

    async def stop(self):
        await super().stop()


Abishnoi = App()
