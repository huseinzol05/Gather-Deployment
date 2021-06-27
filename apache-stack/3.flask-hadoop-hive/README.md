## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Open new terminal,
```bash
compose/bash
python3 app.py
curl http://localhost:5000/employee/Gopal/
```
```text
[[1201, "Gopal", "45000", "Technical manager"]]
```
