import enum
import os
import shutil
import zipfile
import time
from pathlib import Path

import IP2Location
import requests
from dotenv import load_dotenv
from tqdm import tqdm

from easyi2l.db_type import DBType
from easyi2l.easyi2l import EasyI2L


def main():
    db = EasyI2L.download(DBType.DB11LITEBIN).load()

    # tests
    print(db.get_all("1.1.1.1"))


if __name__ == "__main__":
    main()
