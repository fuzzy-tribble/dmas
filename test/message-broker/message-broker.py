from kafka import KafkaProducer, KafkaConsumer

def test_kafka_broker():
    # Create a Kafka producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    # Send a message
    producer.send('test', b'This is a test message')

    # Create a Kafka consumer
    consumer = KafkaConsumer('test', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')

    # Consume the message
    message = next(consumer)

    # Assert that the message is the one we sent
    assert message.value == b'This is a test message'
