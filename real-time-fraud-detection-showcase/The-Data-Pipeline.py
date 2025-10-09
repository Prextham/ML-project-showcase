# Description:  This file shows the logic of our event-driven pipeline using
#               Apache Kafka, which acts as the system's central nervous system.
# ==============================================================================

from kafka import KafkaProducer, KafkaConsumer
import json
import requests

# --- Part 1: The Producer (The "Town Crier") ---
def get_kafka_producer():
    """
    The producer's job is simple: take a transaction and shout it into our
    Kafka pipeline for any interested service to hear.
    """
    # Connect to our Kafka server and set it up to send messages as JSON.
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer

# --- Part 2: The Consumer (The "Listener") ---
def run_consumer_service():
    """
    The consumer's job is to listen patiently for new transactions, and once
    one arrives, it orchestrates the fraud check by calling our API.
    """
    # We tune our "radio" to the 'transactions' channel on our Kafka server.
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest', # Start from the beginning of the stream.
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    API_ENDPOINT = "http://127.0.0.1:8000/predict"

    print("Consumer is now listening for transactions...")
    # This loop will run forever, waiting for new messages.
    for message in consumer:
        transaction = message.value

        # The consumer doesn't do the thinking itself. It acts as a manager,
        # passing the work to our specialist—the API—to get the prediction.
        response = requests.post(API_ENDPOINT, json=transaction)
        prediction = response.json()

        if prediction.get("is_fraud") == 1:
            print(f"!!! FRAUD ALERT DETECTED !!!")
        else:
            print("Transaction processed: Legitimate.")
