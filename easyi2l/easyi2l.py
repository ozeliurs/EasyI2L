import shutil
import time
import zipfile
from pathlib import Path

import requests

from easyi2l.config import db_folder, IP2LOCATION_URL, IP2LOCATION_TOKEN
from easyi2l.db import EasyI2LDB
from easyi2l.db_type import DBType
from easyi2l.logger import logging


class EasyI2L:
    @staticmethod
    def download(database_code: DBType, api_key: str = None) -> EasyI2LDB:
        # If the file already exists and is a file and is not older than 30 days, return the file
        if (
                (db_folder / database_code["file"]).exists() and
                (db_folder / database_code["file"]).is_file() and
                (db_folder / f"{database_code['file']}.timestamp").exists() and
                (db_folder / f"{database_code['file']}.timestamp").is_file() and
                (time.time() - float(
                    (db_folder / f"{database_code['file']}.timestamp").read_text()) < 30 * 24 * 60 * 60)
        ):
            logging.info(f"Using existing {database_code['file']}")
            return EasyI2LDB(database_code["file"])
        else:
            if (db_folder / database_code["file"]).exists():
                (db_folder / database_code["file"]).unlink()
            if (db_folder / f"{database_code['file']}.timestamp").exists():
                (db_folder / f"{database_code['file']}.timestamp").unlink()

        # Use provided api_key if given, otherwise fallback to config
        token = api_key if api_key is not None else IP2LOCATION_TOKEN
        if not token:
            logging.error("Please provide IP2LOCATION_TOKEN as a parameter or set the environment variable")
            raise ValueError("Please provide IP2LOCATION_TOKEN as a parameter or set the environment variable")

        url = IP2LOCATION_URL.format(TOKEN=token, DATABASE_CODE=database_code["code"])
        response = requests.get(url, stream=True)

        # Check if the response is a zip file
        if response.headers.get('Content-Type') != 'application/zip':
            raise ValueError(
                f"Expected a zip file, but got {response.headers.get('Content-Type')}\n\tUrl: {url}\n\tCode: {response.status_code}\n\tContent: {response.content}")

        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 1024
            downloaded_size = 0
            with open(f"{database_code['code']}.zip", "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    downloaded_size += len(data)
                    logging.info(f"Downloading {database_code['code']}.zip: {downloaded_size / total_size:.2%}")

            logging.info(f"Downloaded {database_code['code']}.zip")

            with zipfile.ZipFile(f"{database_code['code']}.zip", "r") as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith(('.BIN', '.CSV')):
                        zip_ref.extract(file_info, ".")
                        logging.info(f"Extracted {file_info.filename}")

                        extracted_file = Path(file_info.filename)
                        shutil.move(str(extracted_file), str(db_folder / extracted_file.name))
                        logging.info(f"Moved {extracted_file.name} to {db_folder}")

                        # Create timestamp file
                        Path(db_folder / f"{extracted_file.name}.timestamp").write_text(str(time.time()))

            logging.info(f"Downloaded and extracted {database_code['code']}.zip")
            Path(f"{database_code['code']}.zip").unlink()

        else:
            raise ValueError(
                f"Failed to download {database_code['code']}.zip\n\tUrl: {url}\n\tCode: {response.status_code}")

        return EasyI2LDB(database_code['file'])
