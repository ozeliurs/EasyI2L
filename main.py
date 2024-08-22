from easyi2l import EasyI2L, DBType


def main():
    db = EasyI2L.download(DBType.DB1LITEBIN).load()

    # Retrieve all data for IP
    print(db.get_all("1.1.1.1"))


if __name__ == "__main__":
    main()
