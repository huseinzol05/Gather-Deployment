import logging
import os
import shutil
import sys
import tempfile

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings, DataTypes
from pyflink.table.descriptors import FileSystem, OldCsv, Schema
from pyflink.table.types import DataTypes

content = (
    'line Licensed to the Apache Software Foundation ASF under one '
    'line or more contributor license agreements See the NOTICE file '
    'line distributed with this work for additional information '
    'line regarding copyright ownership The ASF licenses this file '
    'to you under the Apache License Version the '
    'License you may not use this file except in compliance '
    'with the License'
)

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(
    env,
    environment_settings = EnvironmentSettings.new_instance()
    .use_blink_planner()
    .build(),
)

result_path = '/notebooks/output.csv'

print('Results directory:', result_path)

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
