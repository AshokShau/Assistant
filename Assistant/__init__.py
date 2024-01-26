import logging
from time import time

from config import DEBUG, SUDO_USER

if DEBUG:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
        level=logging.INFO,
    )
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.ERROR)


LOGGER = logging.getLogger(__name__)


StartTime = time()

SUDO_USERS = SUDO_USER
