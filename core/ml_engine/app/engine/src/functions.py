import pyspark.sql.functions as f
from pyspark.sql import DataFrame
from pyspark.ml.linalg import (
    VectorUDT,
    DenseVector,
)


def prepare(dataset: DataFrame, row_name: str, prepared_row_name: str) -> DataFrame:
    return dataset.filter(
        dataset[row_name].isNotNull()
    ).select(
        '*',
        f.split(
            f.col(row_name),
            ' '
        ).alias(
            prepared_row_name
        )
    )


def vector_to_column(vector: DenseVector):
    return f.udf(
        lambda: vector,
        VectorUDT()
    )()
