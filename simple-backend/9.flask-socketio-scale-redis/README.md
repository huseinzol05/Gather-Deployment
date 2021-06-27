## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Run stress test,
```python
# gunicorn with eventlet, 400 unique threads, 100 threads per second
stress_test(400,100)
```
```text
# index 0, total time taken 99.869447 s, average time taken 0.998694 s
# index 100, total time taken 222.226329 s, average time taken 2.222263 s
# index 200, total time taken 271.741829 s, average time taken 2.717418 s
# index 300, total time taken 376.807925 s, average time taken 3.768079 s
```
