NUM_WORKER=$1
BIND_ADDR=0.0.0.0:8008

gunicorn --timeout 120 --log-level=debug -w $NUM_WORKER -b $BIND_ADDR -k eventlet app
