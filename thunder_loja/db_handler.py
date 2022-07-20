#!/usr/bin/python3

import logging
import threading
import psycopg2
from configparser import ConfigParser

from .singleton import Singleton


class DBHandler(metaclass=Singleton):
    def initialise(self, config_file: str, config_section: str):
        self._db_lock = threading.Lock()
        self._config_file = config_file
        self._config_section = config_section
        self._conn = None

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
        self._db_lock.acquire()
        
        try:
            # read connection parameters
            params = self._config()

            # connect to the PostgreSQL server
            self._logger.info('Connecting to the PostgreSQL database...')
            self._conn = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

            if self._conn is not None:
                self._conn.close()
                self._conn = None
                self._db_lock.release()
                self._logger.info('Database connection closed')

        return self._conn


    def disconnect(self):
        """ Disconnect to the PostgreSQL database server """

        if self._conn is not None:
            self._conn.close()
            self._conn = None
            self._logger.info('Database connection closed')

        self._db_lock.release()


    def send_command(self, sql: str):
        """ Receive and send the sql command to the PostgreSQL database server"""

        output = None
        error_msg = None

        try:
            self.connect()
            cur = self._conn.cursor()
            cur.execute(sql)

            try:
                output = cur.fetchall()
            except (Exception, psycopg2.ProgrammingError) as error:
                self._logger.debug(error)
            
            self._conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)
            error_msg = str(error)
        finally:
            self.disconnect()
        
        return output, error_msg


    def send_script(self, sql_script: str):
        sql_commands = self.sql_script_to_array(sql_script)
        
        if sql_commands is None:
            return None

        output = None
        error_msg = None

        try:
            self.connect()
            
            cur = self._conn.cursor()
            for cmd in sql_commands:
                cur.execute(cmd)
            
            try:
                output = cur.fetchall()
            except (Exception, psycopg2.ProgrammingError) as error:
                self._logger.debug(error)

            self._conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)
            error_msg = str(error)
        finally:
            self.disconnect()

        return output, error_msg


    def sql_script_to_array(self, sql_script: str):
        sql_file = None

        try:
            with open(sql_script, 'r') as file:
                sql_file = file.read()
        except FileNotFoundError:
            self._logger.error("File not found")
            return None

        # Remove new lines, split commands and remove empty commands
        sql_commands = sql_file.replace('\n','').split(';')
        sql_commands = [i for i in sql_commands if i]

        return sql_commands


    def test_connection(self):
        self.connect()

        if self._conn is not None:
            # create a cursor
            cur = self._conn.cursor()
            
            # execute a statement
            self._logger.info('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            self._logger.info(db_version)
        
            # close the communication with the PostgreSQL
            cur.close()
            self.disconnect()

            return True
        
        return False
