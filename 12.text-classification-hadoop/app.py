import os
import pydoop.hdfs as hdfs
import json

print(hdfs.hdfs().list_directory('/user'))

with open('text.txt', 'r') as fopen:
    hdfs.dump(fopen.read(), '/user/input_text/text')
os.system(
    "pydoop script --num-reducers 0 -t '' classification.py /user/input_text /user/output_text"
)
list_files = hdfs.hdfs().list_directory('/user/output_text')
with open('output.txt', 'w') as fopen:
    fopen.write(
        json.dumps(
            [
                hdfs.load(file['name'], mode = 'rt')
                for file in list_files
                if 'SUCCESS' not in file['name']
            ]
        )
    )
