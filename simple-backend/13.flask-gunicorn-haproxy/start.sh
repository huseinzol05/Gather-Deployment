NUM_WORKER=$1
BIND_ADDR=0.0.0.0:5000
python3 initial.py
gunicorn --graceful-timeout 30 --reload --max-requests 10 --timeout 180 -w $NUM_WORKER -b $BIND_ADDR -k sync app
