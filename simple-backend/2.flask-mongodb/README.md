## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Try some examples,
```bash
curl localhost:5000/ -x GET
```
```text
Hey, we have Flask with MongoDB in a Docker container!
```
```bash
curl localhost:5000/insert?name=husein -X GET
```
```text
done inserted husein
```
```bash
curl localhost:5000/get?name=husein -X GET
```
```text
husein
```
