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
Hey, we have Flask with Redis in a Docker container!
```
```bash
curl localhost:5000/first-channel -d "data=from first channel" -X PUT
```
```text
"from first channel"
```
