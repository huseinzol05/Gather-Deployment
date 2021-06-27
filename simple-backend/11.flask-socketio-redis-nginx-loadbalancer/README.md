## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Run stress test,
```text
Port 80 will load balanced on 2 different servers, 5000 and 5001.

stress_test(get_time_80, 50,10)
index 0, total time taken 1.087309 s, average time taken 0.108731 s
index 10, total time taken 1.203958 s, average time taken 0.120396 s
index 20, total time taken 1.310126 s, average time taken 0.131013 s
index 30, total time taken 1.595863 s, average time taken 0.159586 s
index 40, total time taken 1.548332 s, average time taken 0.154833 s
```
