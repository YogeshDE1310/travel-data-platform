from utils.logger import logger

from ingestion.extract_api_data import main as extract_main
from ingestion.upload_to_s3 import main as upload_main


def main():

    logger.info("=" * 70)
    logger.info("Travel Data Ingestion Pipeline Started")

    # ----------------------------------------
    # Step 1 : Extract Data
    # ----------------------------------------

    extracted_files = extract_main()

    if not extracted_files:

        logger.error("Extraction failed. Upload skipped.")

        return

    logger.info(f"{len(extracted_files)} files extracted successfully.")

    # ----------------------------------------
    # Step 2 : Upload to S3
    # ----------------------------------------

    upload_main()

    logger.info("Travel Data Ingestion Pipeline Completed")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()