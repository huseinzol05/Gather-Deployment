import logging
import os
import shutil
import sys
import tempfile
import tensorflow as tf

from pyflink.dataset import ExecutionEnvironment
from pyflink.table import BatchTableEnvironment, TableConfig
from pyflink.table.descriptors import FileSystem, OldCsv, Schema
from pyflink.table.types import DataTypes


def word_count():
    content = (
        'line Licensed to the Apache Software Foundation ASF under one '
        'line or more contributor license agreements See the NOTICE file '
        'line distributed with this work for additional information '
        'line regarding copyright ownership The ASF licenses this file '
        'to you under the Apache License Version the '
        'License you may not use this file except in compliance '
        'with the License'
    )

    t_config = TableConfig()
    env = ExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    t_env = BatchTableEnvironment.create(env, t_config)

    # register Results table in table environment
    tmp_dir = tempfile.gettempdir()
    result_path = '/files/output.csv'

    logging.info('Results directory: %s', result_path)

    t_env.connect(FileSystem().path(result_path)).with_format(
        OldCsv()
        .field_delimiter(',')
        .field('word', DataTypes.STRING())
        .field('count', DataTypes.BIGINT())
    ).with_schema(
        Schema()
        .field('word', DataTypes.STRING())
        .field('count', DataTypes.BIGINT())
    ).register_table_sink(
        'Results'
    )

    elements = [(word, 1) for word in content.split(' ')]

    t_env.from_elements(elements, ['word', 'count']).group_by('word').select(
        'word, count(1) as count'
    ).insert_into('Results')

    t_env.execute('word_count')


if __name__ == '__main__':
    logging.basicConfig(
        stream = sys.stdout, level = logging.INFO, format = '%(message)s'
    )

    word_count()
