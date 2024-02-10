import logging
import config

from time import time


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
