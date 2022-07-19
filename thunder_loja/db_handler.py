#!/usr/bin/python3

import logging
import psycopg2
from configparser import ConfigParser

class DBHandler():
    def __init__(self, config_file: str, config_section: str):
        self._config_file = config_file
        self._config_section = config_section

        self._logger = logging.getLogger("DBHandler")


    def _config(self) -> dict:
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self._config_file)

        # get section, default to postgresql
        db = {}
        if parser.has_section(self._config_section):
            params = parser.items(self._config_section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self._config_section, self._config_file))

        return db


    def connect(self) -> psycopg2.extensions.connection:
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = self._config()

            # connect to the PostgreSQL server
            self._logger.info('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

            if conn is not None:
                conn.close()
                self._logger.info('Database connection closed')

        return conn


    def send_command(self, sql: str):
        """ Receive and send the sql command to the PostgreSQL database server"""
        conn = None
        try:
            conn = self._connect
            cur = conn.cursor()
            for cmd in sql:
                cur.execute(cmd)
            output = cur.fetchall()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)
        finally:
            if conn is not None:
                conn.close()
        return output


    def test_connection(self):
        conn = self.connect()

        if conn is not None:
            # create a cursor
            cur = conn.cursor()
            
            # execute a statement
            self._logger.info('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            self._logger.info(db_version)
        
            # close the communication with the PostgreSQL
            cur.close()
            conn.close()

            return True
        
        return False
