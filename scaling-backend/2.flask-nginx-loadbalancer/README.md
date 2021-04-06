## How-to

1. Run `Docker compose`,
```bash
compose/build
```

Port 80 will load balanced on 2 different servers, 5000 and 5001.

```text
curl http://localhost:5000/ -X GET
Hello World! I have been seen 19 times.

curl http://localhost:5001/ -X GET
Hello World! I have been seen 20 times.

curl http://localhost/ -X GET
Hello World! I have been seen 21 times.
```
