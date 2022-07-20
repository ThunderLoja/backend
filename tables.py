#!/usr/bin/python3

import logging
import argparse
from thunder_loja.db_handler import DBHandler

CREATE_TABLES_SCRIPT = 'thunder_loja/scripts/create_tables.sql'
DROP_TABLES_SCRIPT = 'thunder_loja/scripts/drop_tables.sql'
FILL_TABLES_SCRIPT = 'thunder_loja/scripts/fill_tables.sql'

logger = logging.getLogger("Tables")

def execute_script(db_handler: DBHandler, script: str):
    sql_file = None

    try:
        with open(script, 'r') as file:
            sql_file = file.read()
    except FileNotFoundError:
        logger.error("File not found")
        return False

    # Remove new lines, split commands and remove empty commands
    sql_commands = sql_file.replace('\n','').split(';')
    sql_commands = [i for i in sql_commands if i]

    conn = db_handler._connect()
    
    if conn is not None:
        cur = conn.cursor()

        # Execute every command from the input file
        for command in sql_commands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                cur.execute(command)
            except Exception as e:
                logger.error(f"Command skipped: {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        return True

    return False


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", metavar="A", type=str,
                        help="Action to perform ('create', 'drop', 'fill')")

    args = parser.parse_args()

    return args.action


def main():
    action = parse_arguments()

    db_handler = DBHandler(config_file="cfg/database.ini",
                           config_section="thunder_loja_db")

    script_file = None

    if action == 'create':
        logger.info('Creating tables')
        script_file = CREATE_TABLES_SCRIPT
    elif action == 'drop':
        logger.info('Dropping tables')
        script_file = DROP_TABLES_SCRIPT
    elif action == 'fill':
        logger.info('Filling tables')
        script_file = FILL_TABLES_SCRIPT
    else:
        logger.error('Argument not suported')
    
    if script_file is not None:
        execute_script(db_handler, script_file)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()