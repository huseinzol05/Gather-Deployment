import json

with open('dictionary-test.json', 'r') as fopen:
    dic = json.load(fopen)


def mapper(_, record, writer):
    val = dic[record] if record in dic else UNK
    writer.emit('', str(val))
