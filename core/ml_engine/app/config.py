import os

APP_NAME = 'WORD_TO_VEC_TRAIN'


TABLE_NAME = os.environ['TABLE_NAME']
FILE_PATTERN = os.environ['FILE_PATTERN']
ROW_NAME = os.environ['ROW_NAME']

HIVE_CONNECTION_ARGS = (
    "spark.sql.uris",
    f'{os.environ["HIVE_HOST"]}:{os.environ["HIVE_PORT"]}'
)

PREPARED_ROW_NAME = 'tokens'

MODEL_ARGS = {
    'inputCol': PREPARED_ROW_NAME,
    'outputCol': "vectors",
    'vectorSize': 100,
    'minCount': 1,
}
