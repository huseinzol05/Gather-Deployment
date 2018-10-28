#!/usr/bin/python3

import json
import sys

sys.path.append('.')

with open('dictionary-test.json', 'r') as fopen:
    dic = json.load(fopen)

for line in sys.stdin:
    sentences = line.split('\n')
    for sentence in sentences:
        for word in sentence.split():
            val = dic[word] if word in dic else 'UNK'
            print(val)
