#!/usr/bin/env python3

import json

from src.film_parser import FilmParser
from src.hive_connector import HiveConnector
from config import (
    DATA_PATH,
    HOST,
    PORT,
    DB_USER,
    DB_NAME,
    INIT_BD
)


def test_crud(connector, jsons):
    film_json = json.loads(jsons[0])
    film_json['id'] = '111'
    film_json['Star'] = 'NULL'
    film_json['Writer'] = 'NULL'
    film_json['Rating'] = 'NULL'
    film_json['Director'] = 'Joe Mama'
    film_json['Description'] = 'NULL'
    film_json['Name'] = 'NULL'
    film_json = json.dumps(film_json)
    connector.insert_row(film_json, "FILM_CREW")

    search_json = {"id": '111', "Director": 'Joe Mama'}
    search_json = json.dumps(search_json)

    print(connector.select_row(search_json, "FILM_CREW"))

    # uncomment in order to view an error xD
    # connector.delete_row(film_json, "FILM_CREW")
    # print(connector.select_row(film_json, "FILM_CREW"))


def process() -> None:
    pass


def main():
    # You can specify host, port, db_user and db_name variables here
    connector = HiveConnector(HOST, PORT, DB_USER, DB_NAME)
    connector.initialize_connection(INIT_BD)
    parser = FilmParser(DATA_PATH)
    jsons = parser.get_films()

    for film in jsons:
        # Uncomment to see film jsons
        print(film)
        connector.insert_row(film, "FILM_GENERAL")
        connector.insert_row(film, "FILM_CREW")

    # uncomment to test crud operations
    # test_crud(connector, jsons)

    # uncomment to view db after insert operations
    # print(connector.show_tables())

    # uncomment to view db after insert operations
    # print(connector.describe_tables())


if __name__ == '__main__':
    main()
