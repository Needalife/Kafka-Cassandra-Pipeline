import requests,os,time,json
from kafka import KafkaProducer

def get_random_math_fact():
    base_url = 'http://numbersapi.com/random/math?json'
    response = requests.get(base_url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "number": data['number'],
            "text": data['text']
        }
    else:
        return f'Failed to fetch math fact, status code: {response.status_code}'

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

def run():
    count = 0
    print("Setting up math facts producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )

    while True:        
        # adding prints for debugging in logs
        print(f"Sending new math fact data count no:{count}")
        fact = get_random_math_fact()
        print(fact)
        producer.send(TOPIC_NAME, value=fact)
        print("New math data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        count += 1

if __name__ == "__main__":
    run()
