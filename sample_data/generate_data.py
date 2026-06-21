from faker import Faker
import pandas as pd
import random
import uuid
from datetime import timedelta
import os

fake = Faker()

NUM_USERS = 100000
NUM_FLIGHTS = 2000
NUM_HOTELS = 1000
NUM_BOOKINGS = 300000

os.makedirs("../api/data", exist_ok=True)

# --------------------------------
# USERS
# --------------------------------

users = []

for i in range(NUM_USERS):

    users.append({
        "user_id": str(uuid.uuid4()),
        "name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "state": fake.state(),
        "country": fake.country(),
        "signup_date": str(fake.date_between(start_date='-3y', end_date='today')),
        "loyalty_tier": random.choice(["Silver", "Gold", "Platinum"])
    })

users_df = pd.DataFrame(users)

users_df.to_json(
    "../api/data/users.json",
    orient="records",
    indent=2
)

# --------------------------------
# FLIGHTS
# --------------------------------

cities = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Goa",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Jaipur"
]

airlines = [
    "Indigo",
    "Air India",
    "SpiceJet",
    "Vistara",
    "Akasa Air"
]

flights = []

for i in range(NUM_FLIGHTS):

    source = random.choice(cities)

    destination = random.choice(
        [x for x in cities if x != source]
    )

    flights.append({
        "flight_id": str(uuid.uuid4()),
        "airline": random.choice(airlines),
        "source": source,
        "destination": destination,
        "duration_minutes": random.randint(60, 240),
        "price": random.randint(2500, 18000)
    })

flights_df = pd.DataFrame(flights)

flights_df.to_json(
    "../api/data/flights.json",
    orient="records",
    indent=2
)

# --------------------------------
# HOTELS
# --------------------------------

hotel_names = [
    "Grand Palace",
    "Ocean View",
    "Royal Stay",
    "Luxury Inn",
    "Elite Residency"
]

hotels = []

for i in range(NUM_HOTELS):

    hotels.append({
        "hotel_id": str(uuid.uuid4()),
        "hotel_name": random.choice(hotel_names),
        "city": random.choice(cities),
        "rating": round(random.uniform(3.0, 5.0), 1),
        "price_per_night": random.randint(1500, 12000)
    })

hotels_df = pd.DataFrame(hotels)

hotels_df.to_json(
    "../api/data/hotels.json",
    orient="records",
    indent=2
)

# --------------------------------
# BOOKINGS
# --------------------------------

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Wallet"
]

booking_status = [
    "CONFIRMED",
    "PENDING",
    "CANCELLED"
]

bookings = []

for i in range(NUM_BOOKINGS):

    booking_date = fake.date_between(
        start_date='-2y',
        end_date='today'
    )

    checkin = booking_date + timedelta(
        days=random.randint(1, 30)
    )

    checkout = checkin + timedelta(
        days=random.randint(1, 7)
    )

    amount = random.randint(5000, 50000)

    discount = random.randint(0, 5000)

    bookings.append({
        "booking_id": str(uuid.uuid4()),
        "user_id": random.choice(users)["user_id"],
        "flight_id": random.choice(flights)["flight_id"],
        "hotel_id": random.choice(hotels)["hotel_id"],
        "booking_date": str(booking_date),
        "checkin_date": str(checkin),
        "checkout_date": str(checkout),
        "amount": amount,
        "discount": discount,
        "final_amount": amount - discount,
        "payment_method": random.choice(payment_methods),
        "booking_status": random.choice(booking_status)
    })

bookings_df = pd.DataFrame(bookings)

bookings_df.to_json(
    "../api/data/bookings.json",
    orient="records",
    indent=2
)

print("All datasets generated successfully")