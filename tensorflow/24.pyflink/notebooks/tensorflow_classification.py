import logging
import os
import shutil
import sys
import tempfile

from pyflink.dataset import ExecutionEnvironment
from pyflink.table import BatchTableEnvironment, TableConfig, WriteMode
from pyflink.table.descriptors import FileSystem, OldCsv, Schema
from pyflink.table.types import DataTypes

t_config = TableConfig()
env = ExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
t_env = BatchTableEnvironment.create(env, t_config)

source_file = '/notebooks/big-text.txt'
sink_file = '/notebooks/sink.csv'

t_env.connect(FileSystem().path(source_file)).with_format(
    OldCsv().line_delimiter('\n').field('word', DataTypes.STRING())
).with_schema(Schema().field('word', DataTypes.STRING())).register_table_source(
    'mySource'
)

t_env.connect(FileSystem().path(sink_file)).with_format(
    OldCsv()
    .field_delimiter(',')
    .field('word', DataTypes.STRING())
    .field('count', DataTypes.BIGINT())
).with_schema(
    Schema()
    .field('word', DataTypes.STRING())
    .field('count', DataTypes.BIGINT())
).register_table_sink(
    'mySink'
)

t_env.scan('mySource').group_by('word').select('word, count(1)').insert_into(
    'mySink'
)

t_env.execute('wordcount')
