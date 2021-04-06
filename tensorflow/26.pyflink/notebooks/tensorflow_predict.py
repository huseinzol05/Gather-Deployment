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


t_env.set_python_requirements('/notebooks/requirements.txt')

t_env.register_function('predict', predict)

result_path = '/notebooks/output-tensorflow.csv'

t_env.connect(FileSystem().path(result_path)).with_format(
    OldCsv()
    .field_delimiter(',')
    .field('sentence', DataTypes.STRING())
    .field('label', DataTypes.STRING())
).with_schema(
    Schema()
    .field('sentence', DataTypes.STRING())
    .field('label', DataTypes.STRING())
).create_temporary_table(
    'mySink'
)

elements = [(sentence,) for sentence in content.split('\n')]

t_env.from_elements(elements, ['sentence']).select(
    'sentence, predict(sentence)'
).insert_into('mySink')

t_env.execute('predict')
