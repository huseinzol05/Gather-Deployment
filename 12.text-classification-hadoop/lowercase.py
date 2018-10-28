#!/usr/bin/env python3

import sys

for line in sys.stdin:
    sentences = line.split('\n')
    for sentence in sentences:
        print(sentence.strip())
