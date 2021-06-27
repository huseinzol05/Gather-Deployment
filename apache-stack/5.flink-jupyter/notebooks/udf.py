from pyflink.dataset import ExecutionEnvironment
from pyflink.table import TableConfig, DataTypes, BatchTableEnvironment
from pyflink.table.descriptors import Schema, OldCsv, FileSystem
from pyflink.table.types import DataTypes
from pyflink.table.expressions import col, lit
from pyflink.table.udf import udf

with open('/notebooks/big-text.txt') as fopen:
    content = fopen.read()

exec_env = ExecutionEnvironment.get_execution_environment()
t_config = TableConfig()
t_env = BatchTableEnvironment.create(exec_env, t_config)

RANDOM = None


@udf(result_type = DataTypes.STRING())
def concat(string):
    global RANDOM
    from random_word import RandomWords

    if RANDOM is None:
        RANDOM = RandomWords()

    r = RANDOM.get_random_word()
    return f'{r} {string}'


t_env.set_python_requirements('/notebooks/requirements.txt')

t_env.register_function('concat', concat)

result_path = '/notebooks/output-udf.csv'

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
    'concat(word), count(1) as count'
).insert_into('mySink')

t_env.execute('word_count_udf')
