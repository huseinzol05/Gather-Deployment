from transformers import (
    ElectraTokenizer,
    TFElectraModel,
    TFElectraForTokenClassification,
)
import tensorflow as tf
import waterhealer as wh
from streamz import Stream
from typing import List, Tuple
import uuid
import logging
from datetime import datetime
import asyncio
import time

tokenizer = ElectraTokenizer.from_pretrained(
    'monologg/electra-small-finetuned-imdb'
)
model = TFElectraForTokenClassification.from_pretrained(
    'monologg/electra-small-finetuned-imdb', from_pt = True
)
outputs = {}


def to_class(list):
    return {'negative': list[0], 'positive': list[1]}


def classify(rows: List[Tuple[str, str]]):
    """
    rows = [(uuid1, string1), (uuid2, string2)]
    """
    texts = [row[1] for row in rows]
    inputs = tokenizer(texts, return_tensors = 'tf', padding = True)
    outputs = tf.nn.softmax(model(inputs))[0][:, 0, :]
    results = outputs.numpy().tolist()
    return [(rows[i][0], to_class(results[i])) for i in range(len(rows))]


def map_output(rows):
    for row in rows:
        outputs[row[0]] = row[1]


# wait N requests for 0.25 second
# if longer wait, the batch can be really big
global_wait = 0.25

source = Stream()

# https://github.com/huseinzol05/water-healer#partition_time
source.partition_time(global_wait).map(classify).sink(map_output)


async def get(id):
    while True:
        await asyncio.sleep(0.01)
        if id in outputs:
            return outputs.pop(id)


async def batch(string: str):
    logging.info(datetime.now())
    id = str(uuid.uuid4())
    row = (id, string)
    source.emit(row)
    r = await get(id)
    return r


async def element(string: str):
    logging.info(datetime.now())
    inputs = tokenizer(string, return_tensors = 'tf')
    outputs = tf.nn.softmax(model(inputs))[0][:, 0, :]
    results = outputs.numpy().tolist()
    return to_class(results[0])
