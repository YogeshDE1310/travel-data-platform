import os
import json
from datetime import datetime

import requests


from utils.logger import logger

# --------------------------------------------------
# Load Configuration
# --------------------------------------------------

from utils.config_loader import config

BASE_URL = config["api"]["base_url"]
RAW_DATA_FOLDER = config["paths"]["raw_data_folder"]
API_ENDPOINTS = config["apis"]

# --------------------------------------------------
# Create Raw Data Folder
# --------------------------------------------------

os.makedirs(RAW_DATA_FOLDER, exist_ok=True)


# --------------------------------------------------
# Extract API Data
# --------------------------------------------------

def extract_api_data(api_name, endpoint):

    url = BASE_URL + endpoint

    logger.info(f"Calling API : {url}")

    try:

        response = requests.get(url, timeout=30)

        response.raise_for_status()

        data = response.json()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_name = os.path.join(
            RAW_DATA_FOLDER,
            f"{api_name}_{timestamp}.json"
        )

        with open(file_name, "w") as outfile:

            json.dump(
                data,
                outfile,
                indent=4
            )

        logger.info(f"{api_name} extracted successfully.")

        return file_name

    except requests.exceptions.RequestException as e:

        logger.error(f"API Request Failed : {api_name}")

        logger.error(str(e))

        return None

    except Exception as e:

        logger.error(f"Unexpected Error : {api_name}")

        logger.error(str(e))

        return None


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    logger.info("=" * 60)
    logger.info("API Extraction Started")

    extracted_files = []

    for api_name, endpoint in API_ENDPOINTS.items():

        file = extract_api_data(api_name, endpoint)

        if file:

            extracted_files.append(file)

    logger.info("API Extraction Completed")

    logger.info(f"Total Files Extracted : {len(extracted_files)}")

    for file in extracted_files:

        logger.info(file)

    logger.info("=" * 60)
    return extracted_files

if __name__ == "__main__":

    main()