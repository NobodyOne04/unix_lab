#!/bin/bash

export PYSPARK_PYTHON=python3
/bin/bash -c "/usr/local/spark/bin/spark-submit \
    --driver-memory 2g \
    --executor-memory 2g \
    --total-executor-cores 1 \
    --conf 'spark.executor.heartbeatInterval=360000' \
    --conf 'spark.network.timeout=420000' \
    --master spark://172.22.0.4:7077 \
    /app/main.py"
