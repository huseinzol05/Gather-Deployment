## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Try some examples,
```bash
curl localhost:5000/ -d "username=huseinzol05&first_name=husein&last_name=zolkepli&password=comel" -X PUT
```
```text
"success {\"password\": \"comel\", \"first_name\": \"husein\", \"last_name\": \"zolkepli\", \"username\": \"huseinzol05\"}"
```
```bash
curl localhost:5000/ -d "username=huseinzol05" -X GET
```
```text
"[10001, \"huseinzol05\", \"husein\", \"zolkepli\", \"comel\"]"
```
