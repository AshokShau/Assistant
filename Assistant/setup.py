from telegram.ext import Application
from telegram.ext import CommandHandler as CH
from telegram.ext import ExtBot
from telegram.ext import MessageHandler as MH
from telegram.ext import filters

from Assistant import SUDO_USERS as SUDO
from Assistant.modules.broadcast import broadcast, logs, stats
from Assistant.modules.messages import incoming_groups, incoming_private
from Assistant.modules.start import start
from Assistant.modules.sudos import block_func, mode_func, unblock_func


async def setup_(application: Application[ExtBot]) -> None:

    application.add_handler(CH("start", start))
    application.add_handler(CH("logs", logs, filters=filters.User(SUDO)))
    application.add_handler(CH("stats", stats, filters=filters.User(SUDO)))
    application.add_handler(CH("broadcast", broadcast, filters=filters.User(SUDO)))
    application.add_handler(CH("mode", mode_func, filters=filters.User(SUDO)))
    application.add_handler(CH("block", block_func, filters=filters.User(SUDO)))
    application.add_handler(CH("unblock", unblock_func, filters=filters.User(SUDO)))
    application.add_handler(
        MH(
            filters.ChatType.GROUPS & filters.User(SUDO) & ~filters.COMMAND,
            incoming_groups,
        ),
        group=1,
    )
    application.add_handler(
        MH(filters.ChatType.PRIVATE & ~filters.COMMAND, incoming_private),
        group=2,
    )
