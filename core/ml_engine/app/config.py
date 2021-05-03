import os

APP_NAME = 'WORD_TO_VEC_TRAIN'

FILE_PATTERN = os.environ['FILE_PATTERN']
ROW_NAME = os.environ['ROW_NAME']
MODEL_PATH = os.environ['MODEL_PATH']

PREPARED_ROW_NAME = 'tokens'

MODEL_ARGS = {
    'inputCol': PREPARED_ROW_NAME,
    'outputCol': "vectors",
    'vectorSize': 100,
    'minCount': 1,
}
