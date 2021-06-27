## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Try some examples,
```bash
curl localhost:5000 -X GET
```
```text
{"hello": "world"}
```
```bash
curl localhost:5000/todo1 -d "data=take milk" -X PUT
curl localhost:5000/todo1 -X GET
```
```text
{"todo1": "take milk"}
```
