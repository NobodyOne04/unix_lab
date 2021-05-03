import numpy as np
from scipy.spatial.distance import cosine

import pyspark.sql.functions as f
from pyspark.ml.linalg import DenseVector
from pyspark.ml.feature import Word2Vec
from pyspark.sql.types import FloatType
from pyspark.sql import DataFrame

from engine.base import SparkBase
from engine.src.functions import vector_to_column


class SparkWord2Vec(SparkBase):

    def __init__(self, app_name: str, model_args: dict):
        super(SparkWord2Vec, self).__init__(app_name)

        assert model_args.get('inputCol'), 'inputCol must be specified'
        assert model_args.get('outputCol'), 'inputCol must be specified'

        self.__input_col = model_args.get('inputCol')
        self.__output_col = model_args.get('outputCol')
        self.__vector_size = model_args.get('vectorSize', 100)

        self.__word2vec = Word2Vec(**model_args)

        self.__similarity = f.udf(
            self._similarity,
            FloatType()
        )

    def fit(self, df: DataFrame) -> None:
        self.__model = self.__word2vec.fit(
            df
        )
        self.__vectorized = self.__model.transform(df)

    def _query_vector(self, sentence: str) -> DenseVector:
        result_vector = DenseVector(
            np.zeros(
                (self.__vector_size,)
            )
        )
        vectors: DataFrame = self.__model.getVectors()

        for word in sentence.split():
            word_vector: list = vectors.filter(
                vectors.word == word
            ).rdd.map(
                lambda x: x['vector']
            ).collect()

            if word_vector:
                result_vector += word_vector[0]

        return result_vector

    @staticmethod
    def _similarity(vector1: DenseVector, vector2: DenseVector) -> float:
        return float(
            cosine(
                vector1.toArray(),
                vector2.toArray()
            )
        )

    def save(self, path_to_mode: str) -> None:
        # TODO: Доделать как только будет HIVE
        raise NotImplementedError('Save method not yet defined!')

    def get_most_similar(self, sentence: str, index_row: str, number: int = 10) -> DataFrame:
        sentence_vector = self._query_vector(sentence)
        main_rows = self.__vectorized.select(
            self.__vectorized[self.__output_col],
            self.__vectorized[index_row]
        ).withColumn(
            "calculated_vector",
            vector_to_column(sentence_vector)
        )
        weighted = main_rows.withColumn(
            "score",
            self.__similarity(
                'calculated_vector',
                self.__output_col
            )
        )

        return weighted.sort(
            "score"
        ).select(
            index_row
        ).rdd.map(
            lambda x: x[index_row]
        ).take(number)
