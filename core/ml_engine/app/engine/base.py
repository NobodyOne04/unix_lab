from pyspark.context import SparkContext
from pyspark.sql import (
    SparkSession,
    DataFrame,
)


class SparkBase:

    def __init__(self, app_name: str, hive_connection_args: tuple):
        self.spark = SparkSession.builder.appName(
            app_name
        ).enableHiveSupport().config(
            hive_connection_args
        ).getOrCreate()

        self.sc = SparkContext.getOrCreate()

    def read_json_data(self, file_pattern: str) -> DataFrame:
        return self.spark.read.option(
            "multiLine",
            True
        ).json(
            file_pattern
        )
