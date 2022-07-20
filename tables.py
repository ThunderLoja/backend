#!/usr/bin/python3

import logging
import argparse
from thunder_loja.db_handler import DBHandler


CREATE_TABLES_SCRIPT = 'thunder_loja/scripts/create_tables.sql'
DROP_TABLES_SCRIPT = 'thunder_loja/scripts/drop_tables.sql'
FILL_TABLES_SCRIPT = 'thunder_loja/scripts/fill_tables.sql'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", metavar="A", type=str,
                        help="Action to perform ('create', 'drop', 'fill')")

    args = parser.parse_args()

    return args.action


def main():
    logger = logging.getLogger("Tables")
    action = parse_arguments()

    db_handler = DBHandler()

    db_handler.initialise(config_file="cfg/database.ini",
                          config_section="thunder_loja_db")

    if action == 'create':
        logger.info('Creating tables')
        db_handler.send_script(CREATE_TABLES_SCRIPT)
    elif action == 'drop':
        logger.info('Dropping tables')
        db_handler.send_script(DROP_TABLES_SCRIPT)
    elif action == 'fill':
        logger.info('Filling tables')
        db_handler.send_script(FILL_TABLES_SCRIPT)
    else:
        logger.error('Argument not suported')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()