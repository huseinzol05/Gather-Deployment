from pyflink.dataset import ExecutionEnvironment
from pyflink.table import TableConfig, DataTypes, BatchTableEnvironment
from pyflink.table.descriptors import Schema, OldCsv, FileSystem
from pyflink.table.types import DataTypes
from pyflink.table.expressions import col, lit

with open('/notebooks/big-text.txt') as fopen:
    content = fopen.read()

exec_env = ExecutionEnvironment.get_execution_environment()
exec_env.set_parallelism(1)
t_config = TableConfig()
t_env = BatchTableEnvironment.create(exec_env, t_config)

result_path = '/notebooks/output.csv'

t_env.connect(FileSystem().path(result_path)).with_format(
    OldCsv()
    .field_delimiter(',')
    .field('word', DataTypes.STRING())
    .field('count', DataTypes.BIGINT())
).with_schema(
    Schema()
    .field('word', DataTypes.STRING())
    .field('count', DataTypes.BIGINT())
).create_temporary_table(
    'mySink'
)

elements = [(word, 1) for word in content.split(' ')]

t_env.from_elements(elements, ['word', 'count']).group_by(col('word')).select(
    'word, count(1) as count'
).insert_into('mySink')

t_env.execute('word_count')
