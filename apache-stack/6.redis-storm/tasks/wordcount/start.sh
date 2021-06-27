#!/bin/bash

supervisord -c supervisord.conf

while true ; do
  if sparse submit --debug -e prod -n wordcount -w 4; then
    break
  fi
  sleep 2
done

export PYTHONUNBUFFERED=0
python3 ps.py
