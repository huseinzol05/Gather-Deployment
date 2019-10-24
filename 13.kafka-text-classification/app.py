from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'polarities',
    auto_offset_reset = 'earliest',
    bootstrap_servers = ['localhost:9092'],
    api_version = (0, 10),
    consumer_timeout_ms = 1000,
)

print([msg.value.decode('utf-8') for msg in consumer])
