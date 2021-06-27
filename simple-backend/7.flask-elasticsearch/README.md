## How-to

1. Run `Docker compose`,
```bash
compose/build
```

2. Try some examples,
```bash
curl localhost:9200/recipes/_search?q=title:salad -X GET
```
```text
{"took":62,"timed_out":false,"_shards":{"total":1,"successful":1,"skipped":0,"failed":0},"hits":{"total":10,"max_score":0.054237623,"hits":[{"_index":"recipes","_type":"salads","_id":"LtlzD2UBBv9LAuM_3gMX","_score":0.054237623,"_source":{"ingredients": [{"step": "1/4 cup basil leaves"}, {"step": "4 cups 1/2-inch cubes watermelon"}, {"step": "2 teaspoons lemon juice"}, {"step": "1/4 teaspoon kosher salt"}, {"step": "1/4 teaspoon chili powder"}], "description": "A quick salad of watermelon and basil. The chili powder plays well with the sweetness of the melon.", "submitter": "Chefthompson.com", "title": "Watermelon Basil Salad", "calories": "10"}}
```
