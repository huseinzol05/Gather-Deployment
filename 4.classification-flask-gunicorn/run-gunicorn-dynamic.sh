NUM_WORKER=$1
BIND_ADDR=0.0.0.0:8033
gunicorn -w $NUM_WORKER -b $BIND_ADDR -p gunicorn.pid api_dynamic:app