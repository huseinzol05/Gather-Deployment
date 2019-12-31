#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()
    if len(line):
        print(line)
