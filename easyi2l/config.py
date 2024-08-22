import os
from pathlib import Path

from dotenv import load_dotenv

from easyi2l.logger import logging

IP2LOCATION_URL = "https://www.ip2location.com/download/?token={TOKEN}&file={DATABASE_CODE}"

# load .env
load_dotenv()

IP2LOCATION_TOKEN = os.getenv("IP2LOCATION_TOKEN")
if not IP2LOCATION_TOKEN:
    logging.warning("Please provide IP2LOCATION_TOKEN environment variable")

db_folder = Path(__file__).parent / "IP2LOCATION"
db_folder.mkdir(parents=True, exist_ok=True)
