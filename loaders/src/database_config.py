#!/usr/bin/env python3

tables = {
    'FILM_GENERAL': {
        'id': 'FILM_ID',
        'Description': 'FILM_DESC',
        'Name': 'FILM_NAME'
    },
    'FILM_CREW': {
        'id': 'FILM_ID',
        'Star': 'FILM_STAR',
        'Rating': 'FILM_RATING',
        'Director': 'FILM_DIRECTOR',
        'Writer': 'FILM_WRITER'
    },
    'FILM_ML': {
        'id': 'FILM_ID',
        'ml_tiny_int': 'FILM_TINY_INT',
        'ml_int': 'FILM_INT',
        'ml_array_int': 'FILM_ARRAY_INT',
        'ml_array_double': 'FILM_ARRAY_DOUBLE',
    }
}

database_scheme = {
    'FILM_GENERAL': {
        'FILM_ID': 'INTEGER',
        'FILM_DESC': 'STRING',
        'FILM_NAME': 'CHAR(255)'
    },
    'FILM_CREW': {
        'FILM_ID': 'INTEGER',
        'FILM_STAR': 'ARRAY<STRING>',
        'FILM_RATING': 'DOUBLE',
        'FILM_DIRECTOR': 'ARRAY<STRING>',
        'FILM_WRITER': 'ARRAY<STRING>'
    },
    'FILM_ML': {
        'FILM_ID': 'INTEGER',
        'FILM_TINY_INT': 'TINYINT',
        'FILM_INT': 'INTEGER',
        'FILM_ARRAY_INT': 'ARRAY<INTEGER>',
        'FILM_ARRAY_DOUBLE': 'ARRAY<DOUBLE>',
    }
}
