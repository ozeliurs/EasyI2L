from enum import Enum


class DBType(Enum):
    pass


for i in [1, 3, 5, 9, 11]:
    for variant in ["BIN", "CSV"]:
        for ip in ["", ".IPV6"]:
            setattr(
                DBType, f"DB{i}LITE{variant}{ip}",
                {
                    "code": f"DB{i}LITE{variant}{ip}",
                    "file": f"IP2LOCATION-LITE-DB{i}{ip}.{variant}"
                }
            )