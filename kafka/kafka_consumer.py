import uuid
import io
import json
import logging
import os
import time
from datetime import datetime, timezone

from kafka import KafkaConsumer
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

logging.getLogger("azure").setLevel(logging.WARNING)

# ==========================================================
# CONFIGURATION
# ==========================================================

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "travel-events"

TENANT_ID = os.environ["AZURE_TENANT_ID"]
CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]
STORAGE_ACCOUNT_NAME = os.environ["AZURE_STORAGE_ACCOUNT"]

FILESYSTEM_NAME = "travel-events"
RAW_DIRECTORY = "raw"

BATCH_SIZE = 100
BATCH_TIMEOUT_SECONDS = 30

# ==========================================================
# ADLS2 CLIENT (Service Principal auth)
# ==========================================================

credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)

service_client = DataLakeServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
    credential=credential,
)
filesystem_client = service_client.get_file_system_client(FILESYSTEM_NAME)

# ==========================================================
# KAFKA CONSUMER
# ==========================================================

def create_consumer(retries=10, delay=5):
    for attempt in range(1, retries + 1):
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
                key_deserializer=lambda x: x.decode("utf-8") if x else None,
                auto_offset_reset="earliest",
                enable_auto_commit=False,
                group_id="travel-consumer",
            )
            logger.info("Connected to Kafka.")
            return consumer
        except Exception as e:
            logger.warning(f"Kafka not ready ({attempt}/{retries}) : {e}")
            time.sleep(delay)
    raise RuntimeError("Unable to connect to Kafka.")

# ==========================================================
# ADLS2 Upload
# ==========================================================

def upload_batch_to_adls(batch):
    if not batch:
        return

    now = datetime.now(timezone.utc)

    dir_path = (
        f"{RAW_DIRECTORY}/year={now.year}/month={now.month:02d}/"
        f"day={now.day:02d}/hour={now.hour:02d}"
    )
    # Add a short UUID suffix so multiple batches in the same second
    # never collide and silently overwrite each other
    unique_suffix = uuid.uuid4().hex[:8]
    file_name = f"travel_events_{now.strftime('%Y%m%d_%H%M%S')}_{unique_suffix}.jsonl"

    buffer = io.StringIO()
    for event in batch:
        buffer.write(json.dumps(event))
        buffer.write("\n")
    data = buffer.getvalue().encode("utf-8")

    directory_client = filesystem_client.get_directory_client(dir_path)
    try:
        directory_client.create_directory()
    except ResourceExistsError:
        pass

    file_client = directory_client.create_file(file_name)
    file_client.append_data(data, offset=0, length=len(data))
    file_client.flush_data(len(data))

    logger.info(
        f"Uploaded {len(batch)} events to "
        f"abfss://{FILESYSTEM_NAME}@{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net/{dir_path}/{file_name}"
    )

# ==========================================================
# Consumer Loop
# ==========================================================

def consume():
    consumer = create_consumer()
    batch = []
    last_flush = time.time()

    logger.info("Consumer started...")

    try:
        while True:
            records = consumer.poll(timeout_ms=1000, max_records=BATCH_SIZE)

            for _, messages in records.items():
                for message in messages:
                    batch.append(message.value)

            flush_by_size = len(batch) >= BATCH_SIZE
            flush_by_time = (time.time() - last_flush) >= BATCH_TIMEOUT_SECONDS

            if batch and (flush_by_size or flush_by_time):
                try:
                    upload_batch_to_adls(batch)
                    consumer.commit()
                    logger.info("Kafka offsets committed.")
                    batch.clear()
                    last_flush = time.time()
                except Exception as e:
                    logger.exception(f"ADLS Upload Failed : {e}")
                    logger.info("Offsets NOT committed.")

    except KeyboardInterrupt:
        logger.info("Stopping Consumer...")

    finally:
        if batch:
            try:
                upload_batch_to_adls(batch)
                consumer.commit()
            except Exception as e:
                logger.exception(e)
        consumer.close()
        logger.info("Consumer stopped.")


if __name__ == "__main__":
    consume()