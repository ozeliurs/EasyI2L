import IP2Location
from pathlib import Path

from easyi2l.config import db_folder


class EasyI2LDB:
    def __init__(self, database_code, folder: Path = db_folder):
        self.database_code = database_code
        self.folder = Path(folder)
        self.database_file = None

    def load(self) -> IP2Location.IP2Location:
        return IP2Location.IP2Location(str(self.folder / self.database_code))

