import requests
import json
import os
from datetime import datetime

apis = {
    "users": "http://127.0.0.1:5000/users",
    "flights": "http://127.0.0.1:5000/flights",
    "hotels": "http://127.0.0.1:5000/hotels",
    "bookings": "http://127.0.0.1:5000/bookings"
}

os.makedirs("raw_data", exist_ok=True)

for api_name, url in apis.items():

    print(f"Extracting {api_name} data...")

    response = requests.get(url)

    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"raw_data/{api_name}_{timestamp}.json"

    with open(file_name, "w") as f:

        json.dump(data, f, indent=2)

    print(f"{api_name} data saved to {file_name}")

print("API extraction completed successfully")