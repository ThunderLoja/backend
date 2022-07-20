import logging
from thunder_loja.db_handler import DBHandler


def main():
    db_handler = DBHandler()

    db_handler.initialise(config_file="cfg/database.ini",
                          config_section="thunder_loja_db")

    db_handler.test_connection()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
