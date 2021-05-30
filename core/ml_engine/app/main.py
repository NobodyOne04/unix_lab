import logging

from engine.word2vec import SparkWord2Vec
from engine.src.functions import prepare
from config import (
    APP_NAME,
    ROW_NAME,
    TABLE_NAME,
    MODEL_ARGS,
    FILE_PATTERN,
    PREPARED_ROW_NAME,
    HIVE_CONNECTION_ARGS,
)


def main() -> None:
    logging.debug('Init spark session')
    model = SparkWord2Vec(
        APP_NAME,
        HIVE_CONNECTION_ARGS,
        MODEL_ARGS
    )
    logging.debug('Load dataset')
    df = model.read_json_data(FILE_PATTERN)
    logging.debug('Prepare data for a model train')
    df = prepare(
        df,
        ROW_NAME,
        PREPARED_ROW_NAME
    )
    logging.debug('Train Word2Vec model')
    model.fit(df)
    logging.debug('Training completed successfully')
    model.save(TABLE_NAME)
    logging.debug('Finish')


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    )
    main()
