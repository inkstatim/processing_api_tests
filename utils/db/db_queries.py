import logging
from typing import Union

from enums.db_tables import Tables
from utils.db.database import Database


class Queries:
    def __init__(self):
        self.db = Database()
        self.logger = logging.getLogger(__name__)

    def select(self, table: Tables, condition_fields: str, condition_value: Union[str, int], select_field='id') \
            -> Union[str, int]:
        # toDO check rowcount != 0
        query = f"SELECT {select_field} FROM {table} WHERE {condition_fields} IN ('{condition_value}') LIMIT 501"
        query_result = self.db.execute_query(query)
        self.logger.info(f"Select operation completed! \n"
                         f"{query}\n"
                         f"Query result: {query_result}")
        return query_result

    def insert(self, table: Tables, insert_data: dict) -> None:
        # toDo check not None values (should be null)
        keys = insert_data.keys()
        values = [f"'{value}'" for value in insert_data.values()]
        query = (f"INSERT INTO {table} ({', '.join(keys)}) "
                 f"VALUES ({', '.join(values)})"
                 .replace("'null'", 'null'))
        self.db.execute_query(query)
        self.logger.info(f"Insert operation completed! \n {query}")

    def delete(self, table: Tables, key_id: int, delete_field='id') -> None:
        query = f"DELETE FROM {table} WHERE {delete_field} = {key_id}"
        self.db.execute_query(query)
        self.logger.info(f"Delete operation completed! \n {query}")
