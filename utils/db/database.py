import logging

import psycopg2

from resources.db_config import db_processing_config


class Database:
    def __init__(self):
        self.connection = None
        self.logger = logging.getLogger(__name__)

    def connect(self):
        try:
            self.connection = psycopg2.connect(**db_processing_config)
        except psycopg2.OperationalError as e:
            error_message = str(e.pgerror) if e.pgerror else str(e)
            raise psycopg2.OperationalError(f"Error connection database: {error_message}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            self.logger.info("Connection was closed!")

    def execute_query(self, query):
        if not self.connection:
            self.connect()

        with self.connection.cursor() as cursor:  # rollback into with
            cursor.execute(query)
            if query.upper().strip().startswith("SELECT"):
                return cursor.fetchall()
            else:
                self.connection.commit()
