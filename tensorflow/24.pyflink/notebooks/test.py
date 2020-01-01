import abc
import collections
import functools
import inspect

from pyflink.java_gateway import get_gateway
from pyflink.table.types import DataType, _to_java_type
from pyflink.util import utils
from notebooks import udf

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


@udf(
    input_types = [DataTypes.STRING()],
    result_type = DataTypes.ARRAY(DataTypes.STRING()),
)
def split(line):
    return [word.lower() for word in line.split(' ')]
