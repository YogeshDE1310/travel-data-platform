"""
customers.py

Generate (once) and persist master customer data, so customer_id -> details
mapping stays stable across producer restarts. Without this, re-running the
producer would silently reshuffle who each customer_id belongs to, breaking
any downstream join.
"""

import json
import os
import random

FIRST_NAMES = [
    "Amit", "Rahul", "Priya", "Neha", "Ankit", "Rohit", "Pooja",
    "Vikas", "Karan", "Sneha", "Anjali", "Ritika", "Nikhil",
    "Aditya", "Yogesh", "Shivam", "Saurabh", "Aman", "Riya", "Shreya",
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Agarwal",
    "Jain", "Mehta", "Bansal", "Patel", "Yadav", "Tyagi",
    "Joshi", "Kapoor", "Malhotra",
]

_CACHE_PATH = os.path.join(os.path.dirname(__file__), "customers_master.json")


def _build_customers(num_customers=10000):
    customers = []
    for customer_id in range(1, num_customers + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        customers.append({
            "customer_id": customer_id,
            "first_name": first,
            "last_name": last,
            "full_name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}{customer_id}@gmail.com",
            "phone": f"9{random.randint(100000000, 999999999)}",
            "home_city_id": random.randint(1, 20),
            "loyalty_tier": random.choice(["Silver", "Gold", "Platinum"]),
        })
    return customers


def generate_customers(num_customers=10000):
    """
    Load customers from a cached JSON file if it exists, otherwise generate
    once and persist. This keeps customer_id -> attributes stable across
    every producer run.
    """
    if os.path.exists(_CACHE_PATH):
        with open(_CACHE_PATH, "r") as f:
            return json.load(f)

    customers = _build_customers(num_customers)
    with open(_CACHE_PATH, "w") as f:
        json.dump(customers, f)
    return customers