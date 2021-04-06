from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings
from pyflink.table.descriptors import (
    Schema,
    Kafka,
    Json,
    Rowtime,
    OldCsv,
    FileSystem,
)
from pyflink.table.udf import udf

s_env = StreamExecutionEnvironment.get_execution_environment()
s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
s_env.set_parallelism(1)

st_env = StreamTableEnvironment.create(
    s_env,
    environment_settings = EnvironmentSettings.new_instance()
    .in_streaming_mode()
    .use_blink_planner()
    .build(),
)

X, Y, sess = None, None, None


@udf(result_type = DataTypes.STRING())
def predict(string):

    global X, Y, sess

    import tensorflow as tf
    import json
    import numpy as np

    def load_graph(frozen_graph_filename):
        with tf.gfile.GFile(frozen_graph_filename, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def)
        return graph

    if X is None or Y is None or sess is None:
        g = load_graph('/notebooks/frozen_model.pb')
        X = g.get_tensor_by_name('import/Placeholder:0')
        Y = g.get_tensor_by_name('import/logits:0')
        sess = tf.Session(graph = g)

    label = ['negative', 'positive']
    maxlen = 50
    UNK = 3

    with open('/notebooks/dictionary-test.json', 'r') as fopen:
        dic = json.load(fopen)

    sentences = [string]

    x = np.zeros((len(sentences), maxlen))
    for i, sentence in enumerate(sentences):
        for no, k in enumerate(sentence.split()[:maxlen][::-1]):
            x[i, -1 - no] = dic.get(k, UNK)
    indices = np.argmax(sess.run(Y, feed_dict = {X: x}), axis = 1)
    return label[indices[0]]


st_env.set_python_requirements('/notebooks/requirements.txt')

st_env.register_function('predict', predict)


st_env.connect(
    Kafka()
    .version('universal')
    .topic('test')
    .start_from_earliest()
    .property('zookeeper.connect', 'zookeeper:2181')
    .property('bootstrap.servers', 'kafka:9092')
).with_format(
    Json()
    .fail_on_missing_field(True)
    .schema(
        DataTypes.ROW(
            [
                DataTypes.FIELD('datetime', DataTypes.STRING()),
                DataTypes.FIELD('text', DataTypes.STRING()),
            ]
        )
    )
).with_schema(
    Schema()
    .field('datetime', DataTypes.STRING())
    .field('text', DataTypes.STRING())
).in_append_mode().register_table_source(
    'source'
)


result_path = '/notebooks/output-tensorflow.csv'

t_env.connect(FileSystem().path(result_path)).with_format(
    OldCsv()
    .field_delimiter(',')
    .field('datetime', DataTypes.STRING())
    .field('sentence', DataTypes.STRING())
    .field('label', DataTypes.STRING())
).with_schema(
    Schema()
    .field('datetime', DataTypes.STRING())
    .field('sentence', DataTypes.STRING())
    .field('label', DataTypes.STRING())
).in_append_mode().register_table_sink(
    'sink'
)

st_env.from_path('source').select(
    'datetime, sentence, predict(sentence)'
).insert_into('sink')

st_env.execute('predict')
