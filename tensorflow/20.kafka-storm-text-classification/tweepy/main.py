from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
from kafka import KafkaProducer
from kafka.partitioner import RoundRobinPartitioner
from datetime import datetime, timedelta
import json
import re
import os
import time

class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            tweet = process_tweet(data)
            if not tweet:
                time.sleep(1)
                return True
            if not publish_kafka(tweet):
                time.sleep(1)
                return True
            time.sleep(1)
            return True
        except Exception as e:
            print('STREAMING exception:', e)
            time.sleep(1)
            return True

    def on_error(self, status):
        print('ERROR STREAMING:', status, ', sleep for 15 mins')
        time.sleep(60 * 15)
        return False
    
def process_tweet(data):
    tweet = json.loads(data)
    text = re.sub(r'[^\x00-\x7F]+', '', tweet['text'])
    tweettime_utc = datetime.strftime(
        datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        + timedelta(hours = 0),
        '%Y-%m-%d %H:%M:%S',
    )
    return {
        'datetime': tweettime_utc.replace(' ', 'T'),
        'text': text
    }

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding = 'utf-8')
        value_bytes = bytes(value, encoding = 'utf-8')
        x = producer_instance.send(topic_name, value = value_bytes)
        producer_instance.flush()
        return True
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))
        return False


def connect_kafka_producer():
    print('connecting to kafka')
    _producer = None
    try:
        _producer = KafkaProducer(
            bootstrap_servers = ['kafka:9092'],
            api_version = (0, 10),
            partitioner = RoundRobinPartitioner(),
        )
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        print('successfully connected to kafka')
        return _producer
    
def publish_kafka(data):
    p = publish_message(
        kafka_producer, 'twitter', 'streaming', json.dumps(data)
    )
    print('published on', data['datetime'])
    return p

kafka_producer = connect_kafka_producer()
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')

access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')

if __name__ == '__main__':
    while True:
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            stream = Stream(auth, l)
            # http://boundingbox.klokantech.com/ -> CSV Raw
            # bounding box of malaysia
            stream.filter(
                locations = [
                    99.8568959909,
                    0.8232449017,
                    119.5213933664,
                    7.2037547089,
                ]
            )
        except Exception as e:
            print('MAIN exception:', e)
            time.sleep(60)
            continue