import json
import os.path
from api.settings import BASE_DIR
import functools
from loaders import hive_connector
from loaders.film_parser import FilmParser
from config import (
    DATA_PATH,
    HOST,
    PORT,
    DB_USER,
    DB_NAME,
    INIT_BD
)

parser = FilmParser(os.path.join(BASE_DIR,
                                 'loaders/' + DATA_PATH))


def singleton(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance

    wrapper.instance = None
    return wrapper


@singleton
class FilmsFromHive:

    def __init__(self):
        self.connector = hive_connector.HiveConnector(HOST, PORT, DB_USER, DB_NAME)
        self.connector.initialize_connection(INIT_BD)


def select_films(film_name=None):
    if film_name is None:
        film_name = 'a'

    films_from_hive = FilmsFromHive()
    film_json = json.dumps({'Name': 'dsa', 'id': '111', 'Description': 'asd'})
    films_from_hive.connector.insert_row(film_json, "FILM_GENERAL")

    film_json = json.dumps({'Name': 'dsasd fa sdfa sdfa', 'id': '111', 'Description': 'asdasd asd'})
    films_from_hive.connector.insert_row(film_json, "FILM_GENERAL")

    search_json = {"Name": film_name}
    search_json = json.dumps(search_json)
    films = films_from_hive.connector.select_row(str(search_json), "FILM_GENERAL")

    films_json_response = {}
    for i in range(len(films)):
        films_json_response[i] = {'id': films[i][0],
                                  'Description': films[i][1],
                                  'Name': films[i][2]}

    print('-------------------------------------------------')
    for film_json_response in films_json_response:
        print(film_json_response)
    print('-------------------------------------------------')
    return films_json_response
