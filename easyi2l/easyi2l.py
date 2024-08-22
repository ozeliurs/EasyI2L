import shutil
import time
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

from easyi2l.config import db_folder, IP2LOCATION_URL, IP2LOCATION_TOKEN
from easyi2l.db import EasyI2LDB
from easyi2l.db_type import DBType


class EasyI2L:
    @staticmethod
    def download(database_code: DBType) -> EasyI2LDB:
        # If the file already exists and is a file and is not older than 30 days, return the file
        if (
                (db_folder / database_code["file"]).exists() and
                (db_folder / database_code["file"]).is_file() and
                (db_folder / f"{database_code['file']}.timestamp").exists() and
                (db_folder / f"{database_code['file']}.timestamp").is_file() and
                (time.time() - float((db_folder / f"{database_code['file']}.timestamp").read_text()) < 30 * 24 * 60 * 60)
        ):
            print(f"Using existing {database_code['file']}")
            return EasyI2LDB(database_code["file"])
        else:
            if (db_folder / database_code["file"]).exists():
                (db_folder / database_code["file"]).unlink()
            if (db_folder / f"{database_code['file']}.timestamp").exists():
                (db_folder / f"{database_code['file']}.timestamp").unlink()

        url = IP2LOCATION_URL.format(TOKEN=IP2LOCATION_TOKEN, DATABASE_CODE=database_code["code"])
        response = requests.get(url, stream=True)

        # Check if the response is a zip file
        if response.headers.get('Content-Type') != 'application/zip':
            raise ValueError(
                f"Expected a zip file, but got {response.headers.get('Content-Type')}\n\tUrl: {url}\n\tCode: {response.status_code}\n\tContent: {response.content}")

        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 1024
            with open(f"{database_code['code']}.zip", "wb") as file, tqdm(
                    desc=f"Downloading {database_code['code']}.zip",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    bar.update(len(data))
            print(f"Downloaded {database_code['code']}.zip")

            with zipfile.ZipFile(f"{database_code['code']}.zip", "r") as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith(('.BIN', '.CSV')):
                        zip_ref.extract(file_info, ".")
                        print(f"Extracted {file_info.filename}")

                        extracted_file = Path(file_info.filename)
                        shutil.move(str(extracted_file), str(db_folder / extracted_file.name))
                        print(f"Moved {extracted_file.name} to {db_folder}")

                        # Create timestamp file
                        Path(db_folder / f"{extracted_file.name}.timestamp").write_text(str(time.time()))

            print(f"Downloaded and extracted {database_code['code']}.zip")
            Path(f"{database_code['code']}.zip").unlink()

        else:
            raise ValueError(
                f"Failed to download {database_code['code']}.zip\n\tUrl: {url}\n\tCode: {response.status_code}")

        return EasyI2LDB(database_code['file'])