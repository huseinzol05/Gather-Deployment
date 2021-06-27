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
Hey, we have Flask in a Docker container!
```
```bash
curl localhost:5000/members/husein/
```
```text
husein
```
