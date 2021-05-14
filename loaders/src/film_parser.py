#!/usr/bin/env python3

import os
import json


class FilmParser:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder

    # create array with jsons from local data folder
    def get_films(self):
        films = []
        files = os.listdir(self.data_folder)
        for file_name in files:
            temp = self.parse_film(file_name, self.data_folder)
            films.append(temp)

        return films

    # create json reading data from a file
    def parse_film(self, file, path='./'):
        with open(os.path.join(path, file), 'r') as f:
            temp = json.load(f)
            film_id = os.path.basename(f.name)
            temp['id'] = int(os.path.splitext(film_id)[0])
            temp = json.dumps(temp).replace('null', '"NULL"')

        return temp
