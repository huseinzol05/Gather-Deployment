#!/usr/bin/env python3

import sys

for line in sys.stdin:
    sentences = list(filter(None, line.split('\n')))
    for sentence in sentences:
        print(sentence.strip())
