#!/bin/bash

cd processing
while true ; do
  if sparse submit --debug -e prod -n processing -w 10; then
    break
  fi
  sleep 2
done

export PYTHONUNBUFFERED=0
python3 ps.py
