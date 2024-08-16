from kafka import KafkaConsumer
import os, json


if __name__ == "__main__":
    print("Starting Math Fact Consumer")
    TOPIC_NAME = os.environ.get("TOPIC_NAME","mathfact")
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
    CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "localhost")
    CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE", "kafkapipeline")

    print("Setting up Kafka consumer at {}".format(KAFKA_BROKER_URL))
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_BROKER_URL])
    
    print('Waiting for msg...')
    for msg in consumer:
        # print('got one!')
        msg = msg.value.decode('ascii')
        jsonData=json.loads(msg)
        print(jsonData)