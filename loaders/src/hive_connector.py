#!/usr/bin/env python3

import json

from pyhive import hive
from src.database_config import tables, database_scheme


def logging(log_str):
    print(f"HIVE LOG: {log_str}")


sql_numeric_types = {'INTEGER', 'DOUBLE', 'TINYINT'}
sql_string_types = {'STRING', 'CHAR'}
sql_string_array_types = {'ARRAY<STRING>'}
sql_numeric_array_types = {'ARRAY<INTEGER>', 'ARRAY<DOUBLE>'}


class HiveConnector:
    # initialize variables for hive connection
    def __init__(self, host='localhost', port=10000, db_user='', db_name='FILMS_DB'):
        self.host = host
        self.port = port
        self.db_user = db_user
        self.db_name = db_name
        self.cursor = None

    # initialize the hive connection itself
    def initialize_connection(self, init_db=False):
        conn = hive.Connection(host=self.host, port=self.port, username=self.db_user)
        self.cursor = conn.cursor()

        if self.cursor is None:
            logging('Can\'t connect to the hive database. Check connection variables')
            return -1

        if init_db:
            self.init_db()
        else:
            self.cursor.execute(f"USE {self.db_name}")

        return 0

    def check_db_exists(self, db_name):
        self.cursor.execute('show databases')
        names = [i[0] for i in self.cursor.fetchall()]

        return db_name.lower() in names

    def clear_db(self):
        for table in database_scheme:
            self.cursor.execute(f"DROP TABLE {table}")
        self.cursor.execute(f"DROP DATABASE {self.db_name}")

    def init_db(self):
        if self.check_db_exists(self.db_name):
            self.cursor.execute(f"USE {self.db_name}")
            logging('Database is already set. Deleting...')
            self.clear_db()

        self.cursor.execute(f"CREATE DATABASE {self.db_name}")
        self.cursor.execute(f"USE {self.db_name}")

        for table in database_scheme:
            self.cursor.execute(self.compose_table_query(table))

        # ACID WARNING: THE QUERY BELOW ENABLES THE TRANSACTION MANAGER TO WORK WITH ACID TABLES
        # self.cursor.execute("""SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;""")

    # compose sql query for the creation of all tables
    def compose_tables_query(self):
        query = ''
        for table in database_scheme:
            query += self.compose_table_query(table)

        return query

    # compose sql query for the table creation
    def compose_table_query(self, table):
        query = f"CREATE TABLE {table} ("
        for field in database_scheme[table]:
            query += f"{field} {database_scheme[table][field]}, "

        query = f"{query[:-2]})"

        # ACID WARNING: THE QUERY BELOW ENABLES THE CREATION OF ACID TABLES
        # query += f"""
        # CLUSTERED BY (FILM_ID) INTO {len(tables[table])} BUCKETS STORED AS ORC
        # TBLPROPERTIES ("transactional"="true",
        # "compactor.mapreduce.map.memory.mb"="2048",
        # "compactorthreshold.hive.compactor.delta.num.threshold"="4",
        # "compactorthreshold.hive.compactor.delta.pct.threshold"="0.5"
        # )"""

        logging(query + '\n')
        return query

    # compose query for select request (e.g. set "WHERE 'film_id' = 1 AND...")
    def compose_where_query(self, json_str, table):
        query = "WHERE "
        query_json = json.loads(json_str)
        # for every key in json
        for i in query_json:
            # get table representation of that key(e.g. 'id' key in FILM_GENERAL table would be "FILM_ID")
            column_name = self.get_table_representation(i, table)
            if column_name is None:
                continue
            # get column type(e.g. "FILM_ID" column in FILM_GENERAL table would have INTEGER Type)
            column_type = self.get_column_type(column_name, table)

            # if column type is numeric array
            if column_type in sql_numeric_array_types:
                logging("WARNING: SEARCH BY NUMERIC ARRAYS IS NOT IMPLEMENTED")
                continue
            # if column type is char array
            elif column_type in sql_string_array_types:
                query += f'concat_ws(\' \', {column_name}) = \"'
                if isinstance(query_json[i], list):
                    for string in query_json[i]:
                        query += f'{string} '
                    query = f"{query[:-1]}\""
                else:
                    query += f'{query_json[i]}\"'
            # if column type is numeric type
            elif column_type in sql_numeric_types:
                query += f'{column_name} = {query_json[i]}'
            # if column type is char type
            elif True in [a in column_type for a in sql_string_types]:
                query += f'{column_name} = "{query_json[i]}"'
            # https://i.kym-cdn.com/entries/icons/facebook/000/032/695/hell.jpg
            else:
                logging(f"ERROR: CANNOT FIND DATA TYPE for {i} parameter in the {table} table."
                        f"Column name: {column_name}. Column type: {column_type}")
                continue
            query += " AND "

        return query[:-4]

    # get sql table column name for the json property in a specified table
    def get_table_representation(self, json_property, table):
        for column in tables[table]:
            if column == json_property:
                return tables[table][column]

    # get sql column type for the sql column in a specified table
    # ALWAYS SPECIFY TABLE IF YOU CAN
    def get_column_type(self, column_name, table=None):
        if table is not None:
            return database_scheme[table][column_name]
        else:
            for table_name in database_scheme:
                for column in database_scheme[table_name]:
                    if column == column_name:
                        return database_scheme[table_name][column]

    def convert_to_sql_form(self, json_row, json_property, table):
        query = ''

        # get json_property (e.g. 'id') return sql type of the corresponding column(e.g., 'INTEGER')
        column_name = self.get_table_representation(json_property, table)
        sql_type = self.get_column_type(column_name, table)

        # check if JSON contains the required field to input in the table or if it even has a value at all
        if json_property not in json_row or json_row[json_property] is None:
            if sql_type[:5] == 'ARRAY':
                return "array('NULL')"
            return "NULL"

        # if column type is numeric
        if sql_type in sql_numeric_types:
            query = json_row[json_property]
        # if column type is char array
        elif sql_type in sql_string_array_types:
            query += 'array('
            if isinstance(json_row[json_property], str):
                insert_str = json_row[json_property].replace('"', "")
                query += f"\"{insert_str}\")"
                return query

            for str_elem in json_row[json_property]:
                insert_str = str_elem.replace('"', "")
                query += f"\"{insert_str}\", "

            query = f"{query[:-2]})"
        # if column type is numeric array
        elif sql_type in sql_numeric_array_types:
            query += 'array('
            for num in json_row[json_property]:
                query += f"{num}, "
            query = f"{query[:-2]})"
        # if column type is char
        elif True in [a in sql_type for a in sql_string_types]:
            insert_str = json_row[json_property].replace('"', "")
            query = f"\"{insert_str}\""
        # https://i.kym-cdn.com/entries/icons/facebook/000/032/695/hell.jpg
        else:
            logging(f"ERROR: WRONG DATA TYPE for {json_property} in the {table} table. DATA TYPE: {sql_type}")
            return None

        # logging(f"column name is {column_name}")
        # logging(f"sql type is {sql_type}")
        # logging(f"sql form is {query}")
        return query

    # compose and execute insert query in a specified table with custom data
    def insert_row(self, json_row, table):
        json_row = json.loads(json_row)
        query = f"INSERT INTO {table} SELECT "
        for column_name in tables[table]:
            sql_form = self.convert_to_sql_form(json_row, column_name, table)
            query += f"{sql_form}, "

        query = query[:-2]
        logging(query)
        self.cursor.execute(query)

    # compose and execute select query in a specified table with custom data
    def select_row(self, search_json, table):
        query = f"SELECT * FROM {table} {self.compose_where_query(search_json, table)}"
        logging(query)
        self.cursor.execute(query)

        return self.cursor.fetchall()

    # compose and execute update query in a specified table with custom data
    def update_row(self, old_json, new_json, table):
        logging("UPDATE FUNCTION IS NOT IMPLEMENTED")
        return None

    # compose and execute delete query in a specified table with custom data
    def delete_row(self, delete_json, table):
        query = f'DELETE FROM FILMS {self.compose_where_query(delete_json, table)}'
        logging(query)
        self.cursor.execute(query)

        return 0

    # return every column and its type of every table in the database
    def describe_tables(self):
        query = ''
        for table in database_scheme:
            query += f'{table} COLUMNS:\n'
            for column_tuple in self.describe_table(table):
                query += ' '.join(column_tuple)
                query += '\n'
            query += '\n'

        return query[:-2]

    # return every column and its type of the specified table in the database
    def describe_table(self, table):
        self.cursor.execute(f"DESCRIBE {table}")
        return self.cursor.fetchall()

    # return name of every table in the database
    def show_tables(self):
        query = f'{self.db_name} TABLES: '
        self.cursor.execute("SHOW TABLES")
        tables_tuple = self.cursor.fetchall()
        for column_tuple in tables_tuple:
            query += f'{column_tuple[0]}, '

        return query[:-2]
