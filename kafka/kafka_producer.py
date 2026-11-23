"""
Kafka Producer

Publishes travel events to Kafka.
"""

import json
import logging
import os
import sys
import time

from kafka import KafkaProducer

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from event_generator.travel_event_generator import generate_event  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

TOPIC = "travel-events"
BOOTSTRAP_SERVERS = "localhost:9092"
EVENTS_PER_SECOND = 10


def create_producer(retries=10, delay=5):
    for attempt in range(1, retries + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                acks="all",
                retries=5,
            )
            logger.info("Connected to Kafka.")
            return producer
        except Exception as e:
            logger.warning(f"Kafka not ready ({attempt}/{retries}) : {e}")
            time.sleep(delay)
    raise RuntimeError("Unable to connect to Kafka.")


def main():
    producer = create_producer()
    logger.info("Travel Producer Started...")

    counter = 0
    try:
        while True:
            event = generate_event()
            # Key by customer_id where present, so all events for the same
            # customer land on the same partition (ordering guarantee per customer)
            key = str(event.get("customer_id", "unknown"))

            producer.send(TOPIC, key=key, value=event)
            counter += 1

            if counter % 10 == 0:
                producer.flush()
                logger.info(f"{counter} events published")

            time.sleep(1 / EVENTS_PER_SECOND)

    except KeyboardInterrupt:
        logger.info("Stopping producer...")
    finally:
        producer.flush()
        producer.close()
        logger.info(f"Producer stopped. Total events published = {counter}")


if __name__ == "__main__":
    main()