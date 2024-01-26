from telegram.ext import Application, CommandHandler, ExtBot, MessageHandler, filters

from Assistant import SUDO_USERS
from Assistant.modules.broadcast import broadcast, stats
from Assistant.modules.messages import incoming_groups, incoming_private
from Assistant.modules.start import start
from Assistant.modules.sudos import block_func, mode_func, unblock_func


async def setup_(application: Application[ExtBot]) -> None:

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("mode", mode_func))
    application.add_handler(CommandHandler("block", block_func))
    application.add_handler(CommandHandler("unblock", unblock_func))
    application.add_handler(
        MessageHandler(
            filters.ChatType.GROUPS & filters.User(SUDO_USERS) & ~filters.COMMAND,
            incoming_groups,
        ),
        group=1,
    )
    application.add_handler(
        MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, incoming_private),
        group=2,
    )
