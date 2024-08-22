import IP2Location

from easyi2l.config import db_folder


class EasyI2LDB:
    def __init__(self, database_code):
        self.database_code = database_code
        self.database_file = None

    def load(self) -> IP2Location.IP2Location:
        return IP2Location.IP2Location(f"{db_folder}/{self.database_code}")