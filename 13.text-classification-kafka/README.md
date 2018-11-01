## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Open new tab / window terminal,
```bash
compose/bash
```

3. Run `producer.py`,
```bash
python3 producer.py
```
```text
connecting to kafka
successfully connected to kafka
feeding i love you so much
Message published successfully.
feeding the story totally disgusting
Message published successfully.
feeding the story is really good
Message published successfully.
feeding the story is a shit
Message published successfully.
feeding
Message published successfully.
```

4. Run `app.py`,
```bash
python3 app.py
```
```text
['negative', 'negative', 'positive', 'positive', 'negative']
```

I tried to implement Kafka-manager developed by Yahoo, but seems some of `jar` cannot download.

![alt text](supervisord.png)
