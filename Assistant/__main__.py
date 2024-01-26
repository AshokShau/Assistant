import asyncio
import importlib
import traceback

from pyrogram import idle

from Assistant import LOGGER, Abishnoi
from Assistant.modules import ALL_MODULES


async def main():
    try:
        await Abishnoi.start()
    except KeyboardInterrupt:
        pass
    except Exception:
        LOGGER.info(traceback.format_exc())
        quit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("Assistant.modules." + all_module)

    LOGGER.info(f"Assistant Started as @{Abishnoi.username}")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    LOGGER.info("Stopping Bot...")
