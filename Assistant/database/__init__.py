from sys import exit

from async_mongo import AsyncClient

from Assistant import LOGGER
from config import DB_URI

try:
    mongo = AsyncClient(DB_URI)
    db = mongo["Assistant"]
    LOGGER.info("Connected to your Mongo Database.")
except Exception as e:
    LOGGER.error(f"Failed to connect to your Mongo Database:{e}")
    exit(1)
