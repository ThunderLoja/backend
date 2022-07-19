import logging
from .connect import db_connect


def main():
    conn = db_connect()

    if conn is not None:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
