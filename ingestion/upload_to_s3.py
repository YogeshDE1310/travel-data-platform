import os

import boto3


from utils.logger import logger

# --------------------------------------------------
# Load Configuration
# --------------------------------------------------

from utils.config_loader import config

BUCKET_NAME = config["aws"]["bucket_name"]
REGION = config["aws"]["region"]
RAW_DATA_FOLDER = config["paths"]["raw_data_folder"]

# --------------------------------------------------
# Create S3 Client
# --------------------------------------------------

s3 = boto3.client(
    "s3",
    region_name=REGION
)


# --------------------------------------------------
# Upload Single File
# --------------------------------------------------

def upload_file(local_file):

    file_name = os.path.basename(local_file)

    dataset = file_name.split("_")[0]

    s3_key = f"bronze/{dataset}/{file_name}"

    logger.info(f"Uploading : {file_name}")

    try:

        s3.upload_file(
            local_file,
            BUCKET_NAME,
            s3_key
        )

        logger.info(
            f"Uploaded Successfully : s3://{BUCKET_NAME}/{s3_key}"
        )

    except Exception as e:

        logger.error(f"Upload Failed : {file_name}")

        logger.error(str(e))


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    logger.info("=" * 60)
    logger.info("S3 Upload Started")

    if not os.path.exists(RAW_DATA_FOLDER):

        logger.error(f"{RAW_DATA_FOLDER} does not exist.")

        return

    files = os.listdir(RAW_DATA_FOLDER)

    if not files:

        logger.warning("No files found to upload.")

        return

    for file in files:

        local_path = os.path.join(
            RAW_DATA_FOLDER,
            file
        )

        upload_file(local_path)

    logger.info("S3 Upload Completed")
    logger.info("=" * 60)
    return True


if __name__ == "__main__":

    main()