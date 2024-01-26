import pytz
from telegram import Update
from telegram._linkpreviewoptions import LinkPreviewOptions
from telegram.constants import ParseMode as PM
from telegram.ext import ApplicationBuilder, Defaults

import config
from Assistant.setup import setup_

defaults = Defaults(
    allow_sending_without_reply=True,
    parse_mode=PM.HTML,
    link_preview_options=LinkPreviewOptions(is_disabled=True),
    block=False,
    tzinfo=pytz.timezone(config.TIME_ZONE),
)


def main() -> None:
    application = (
        ApplicationBuilder()
        .token(config.TOKEN)
        .defaults(defaults)
        .read_timeout(7)
        .get_updates_read_timeout(42)
        .post_init(setup_)
        .build()
    )
    application.run_polling(drop_pending_updates=True, allowed_updates=Update.MESSAGE)


if __name__ == "__main__":
    main()
