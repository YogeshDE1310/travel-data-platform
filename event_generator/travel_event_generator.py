"""
Travel Event Generator

Generates realistic travel events.
"""

import random
import uuid
from datetime import datetime

from event_generator.airlines import AIRLINES
from event_generator.hotels import HOTELS
from event_generator.cities import CITIES
from event_generator.customers import generate_customers

customers = generate_customers()


def booking_event():

    customer = random.choice(customers)

    hotel = random.choice(HOTELS)

    airline = random.choice(AIRLINES)

    source = random.choice(CITIES)

    destination = random.choice(CITIES)

    while destination["city_id"] == source["city_id"]:

        destination = random.choice(CITIES)

    booking_amount = random.randint(4000,30000)

    return {

        "event_type":"BOOKING",

        "event_time":datetime.utcnow().isoformat(),

        "booking_id":str(uuid.uuid4()),

        "customer_id":customer["customer_id"],

        "hotel_id":hotel["hotel_id"],

        "airline_id":airline["airline_id"],

        "source_city_id":source["city_id"],

        "destination_city_id":destination["city_id"],

        "booking_amount":booking_amount,

        "booking_status":"CONFIRMED"

    }


def search_event():

    customer = random.choice(customers)

    source = random.choice(CITIES)

    destination = random.choice(CITIES)

    while destination["city_id"] == source["city_id"]:

        destination = random.choice(CITIES)

    return {

        "event_type":"SEARCH",

        "event_time":datetime.utcnow().isoformat(),

        "search_id":str(uuid.uuid4()),

        "customer_id":customer["customer_id"],

        "source_city_id":source["city_id"],

        "destination_city_id":destination["city_id"]

    }


def payment_event():

    customer = random.choice(customers)

    return {

        "event_type":"PAYMENT",

        "event_time":datetime.utcnow().isoformat(),

        "payment_id":str(uuid.uuid4()),

        "customer_id":customer["customer_id"],

        "amount":random.randint(3000,25000),

        "payment_status":"SUCCESS",

        "payment_method":random.choice(

            ["UPI","Credit Card","Debit Card","Net Banking"]

        )

    }


def cancellation_event():

    customer = random.choice(customers)

    return {

        "event_type":"CANCELLATION",

        "event_time":datetime.utcnow().isoformat(),

        "cancellation_id":str(uuid.uuid4()),

        "customer_id":customer["customer_id"],

        "refund_amount":random.randint(1000,15000),

        "reason":random.choice([

            "Personal",

            "Medical",

            "Flight Delay",

            "Weather"

        ])

    }


def generate_event():

    r = random.random()

    if r < 0.70:

        return booking_event()

    elif r < 0.85:

        return search_event()

    elif r < 0.95:

        return payment_event()

    else:

        return cancellation_event()