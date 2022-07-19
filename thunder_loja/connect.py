#!/usr/bin/python3

import logging
import psycopg2
from configparser import ConfigParser

logger = logging.getLogger("connect")

def config(filename='thunder_loja/cfg/database.ini', section='thunder_loja_db'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def db_connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        logger.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        logger.info('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        logger.info(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)

        if conn is not None:
            conn.close()
            logger.info('Database connection closed.')

    return conn


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    db_connect().close()