import boto3
import os

# Replace with your real bucket name

BUCKET_NAME = "travel-data-lake-yogesh"

# Folder containing extracted raw files

RAW_DATA_FOLDER = "raw_data"

# Create S3 client

s3 = boto3.client("s3")

# Upload all files

for file_name in os.listdir(RAW_DATA_FOLDER):

    local_path = os.path.join(
        RAW_DATA_FOLDER,
        file_name
    )

    # Create Bronze layer paths

    if "users" in file_name:

        s3_path = f"bronze/users/{file_name}"

    elif "flights" in file_name:

        s3_path = f"bronze/flights/{file_name}"

    elif "hotels" in file_name:

        s3_path = f"bronze/hotels/{file_name}"

    elif "bookings" in file_name:

        s3_path = f"bronze/bookings/{file_name}"

    else:
        continue

    print(f"Uploading {file_name}...")

    s3.upload_file(
        local_path,
        BUCKET_NAME,
        s3_path
    )

    print(f"Uploaded to s3://{BUCKET_NAME}/{s3_path}")

print("All files uploaded successfully")