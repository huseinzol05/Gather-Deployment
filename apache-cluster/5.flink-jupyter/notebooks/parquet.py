from pyflink.dataset import ExecutionEnvironment
from pyflink.table import TableConfig, DataTypes, BatchTableEnvironment, EnvironmentSettings
from pyflink.table.descriptors import Schema, OldCsv, FileSystem
from pyflink.table.types import DataTypes
from pyflink.table.expressions import col, lit

t_env = BatchTableEnvironment.create(
    environment_settings=EnvironmentSettings.new_instance()
    .in_batch_mode().use_blink_planner().build())

t_env._j_tenv.getPlanner().getExecEnv().setParallelism(1)

my_source_ddl = f"""
CREATE TABLE mySource (
  registration_dttm TIMESTAMP,
  id INT,
  first_name STRING,
  last_name STRING,
  email STRING,
  gender STRING,
  ip_address STRING,
  cc STRING,
  country STRING,
  birthdate STRING,
  salary DOUBLE,
  title STRING,
  comments STRING
) WITH (
 'connector' = 'filesystem',
 'path' = '/notebooks/userdata1.parquet',
 'format' = 'parquet'
)
"""

my_sink_ddl = f"""
CREATE TABLE mySink (
  registration_dttm TIMESTAMP(6),
  id INT,
  first_name STRING,
  last_name STRING,
  email STRING,
  gender STRING,
  ip_address STRING,
  cc STRING,
  country STRING,
  birthdate STRING,
  salary DOUBLE,
  title STRING,
  comments STRING
) WITH (
 'connector' = 'filesystem',
 'path' = '/notebooks/output',
 'format' = 'csv'
)
"""

t_env.sql_update(my_source_ddl)
t_env.sql_update(my_sink_ddl)

tab = t_env.from_path('mySource')
tab.select('*').insert_into('mySink')

t_env.execute('sink_parquet')

t_env.execute('sink_parquet')