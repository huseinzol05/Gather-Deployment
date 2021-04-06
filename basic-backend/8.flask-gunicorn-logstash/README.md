## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Request url,
```html
http://localhost:9200/_cat/indices?v
```

3. Check index,
```text
health status index               uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   logstash-2018.09.30 IL6UjeHTTCKdL8be5hpOUw   5   1          0            0       460b           460b
```

4. Search on the index,
```html
http://localhost:9200/logstash-2018.09.30/_search
```

```text
{"took":147,"timed_out":false,"_shards":{"total":5,"successful":5,"skipped":0,"failed":0},"hits":{"total":4,"max_score":1.0,"hits":[{"_index":"logstash-2018.09.30","_type":"doc","_id":"lUw4KGYBBCQZE1CyH2wT","_score":1.0,"_source":{"@timestamp":"2018-09-30T02:04:18.472Z","host":"localhost","@version":"1","port":36286,"message":"172.22.0.1 - - [30/Sep/2018:02:04:18 +0000] \"GET / HTTP/1.1\" 200 41 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\""}},{"_index":"logstash-2018.09.30","_type":"doc","_id":"k0w4KGYBBCQZE1CyHWyY","_score":1.0,"_source":{"@timestamp":"2018-09-30T02:04:17.203Z","host":"localhost","@version":"1","port":36286,"message":"172.22.0.1 - - [30/Sep/2018:02:04:16 +0000] \"GET / HTTP/1.1\" 200 41 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\""}},{"_index":"logstash-2018.09.30","_type":"doc","_id":"lkw4KGYBBCQZE1CyH2zP","_score":1.0,"_source":{"@timestamp":"2018-09-30T02:04:18.658Z","host":"localhost","@version":"1","port":36286,"message":"172.22.0.1 - - [30/Sep/2018:02:04:18 +0000] \"GET / HTTP/1.1\" 200 41 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\""}},{"_index":"logstash-2018.09.30","_type":"doc","_id":"lEw4KGYBBCQZE1CyHWzg","_score":1.0,"_source":{"@timestamp":"2018-09-30T02:04:18.160Z","host":"localhost","@version":"1","port":36286,"message":"172.22.0.1 - - [30/Sep/2018:02:04:18 +0000] \"GET / HTTP/1.1\" 200 41 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\""}}]}}
```
