import json
import time
import requests
from kafka import KafkaProducer

# Kafka configuration
KAFKA_TOPIC = "earthquakes"
KAFKA_BROKER = "localhost:9092"

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Free USGS earthquake feed (last 1 hour)
USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

print("Starting earthquake producer...")

while True:
    response = requests.get(USGS_URL)
    data = response.json()

    for feature in data["features"]:
        quake = {
            "id": feature["id"],
            "place": feature["properties"]["place"],
            "magnitude": feature["properties"]["mag"],
            "time": feature["properties"]["time"],
            "longitude": feature["geometry"]["coordinates"][0],
            "latitude": feature["geometry"]["coordinates"][1]
        }

        producer.send(KAFKA_TOPIC, quake)
        print("Sent:", quake)

    producer.flush()
    time.sleep(60)  # fetch every 60 seconds
