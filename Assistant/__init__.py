import logging
from time import time

import pytz
from telegram import Update
from telegram._linkpreviewoptions import LinkPreviewOptions as LPO
from telegram.constants import ParseMode as PM
from telegram.ext import AIORateLimiter, ApplicationBuilder, Defaults, PicklePersistence

import config

# setup logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=config.LOGGER_LEVEL,
)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)


StartTime = time()
SUDO_USERS = config.SUDO_USER

adminlist = {}

defaults = Defaults(
    allow_sending_without_reply=True,
    parse_mode=PM.HTML,
    link_preview_options=LPO(is_disabled=True),
    block=False,
    tzinfo=pytz.timezone(config.TIME_ZONE),
)

persistence = PicklePersistence(filepath="bot_data.pickle")

application = (
    ApplicationBuilder()
    .token(config.TOKEN)
    .defaults(defaults)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .concurrent_updates(True)
    .persistence(persistence)
    .arbitrary_callback_data(True)
    .rate_limiter(
        AIORateLimiter(
            overall_max_rate=0,
            overall_time_period=0,
            group_max_rate=0,
            group_time_period=0,
            max_retries=3,
        )
    )
    .build()
)
