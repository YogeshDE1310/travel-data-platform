"""
hotels.py

Master list of hotels.
Each hotel belongs to one city.
"""

HOTELS = [

    # Delhi
    {
        "hotel_id": 1001,
        "hotel_name": "The Leela Palace",
        "city_id": 1,
        "hotel_rating": 5,
        "price_per_night": 14500
    },
    {
        "hotel_id": 1002,
        "hotel_name": "ITC Maurya",
        "city_id": 1,
        "hotel_rating": 5,
        "price_per_night": 12800
    },
    {
        "hotel_id": 1003,
        "hotel_name": "Holiday Inn Delhi",
        "city_id": 1,
        "hotel_rating": 4,
        "price_per_night": 7200
    },

    # Mumbai
    {
        "hotel_id": 1004,
        "hotel_name": "The Taj Mahal Palace",
        "city_id": 2,
        "hotel_rating": 5,
        "price_per_night": 18500
    },
    {
        "hotel_id": 1005,
        "hotel_name": "The Oberoi Mumbai",
        "city_id": 2,
        "hotel_rating": 5,
        "price_per_night": 16200
    },
    {
        "hotel_id": 1006,
        "hotel_name": "Lemon Tree Mumbai",
        "city_id": 2,
        "hotel_rating": 4,
        "price_per_night": 6800
    },

    # Bengaluru
    {
        "hotel_id": 1007,
        "hotel_name": "The Ritz Carlton",
        "city_id": 3,
        "hotel_rating": 5,
        "price_per_night": 15200
    },
    {
        "hotel_id": 1008,
        "hotel_name": "ITC Gardenia",
        "city_id": 3,
        "hotel_rating": 5,
        "price_per_night": 13500
    },

    # Hyderabad
    {
        "hotel_id": 1009,
        "hotel_name": "Novotel Hyderabad",
        "city_id": 4,
        "hotel_rating": 5,
        "price_per_night": 9800
    },
    {
        "hotel_id": 1010,
        "hotel_name": "Marriott Hyderabad",
        "city_id": 4,
        "hotel_rating": 5,
        "price_per_night": 12100
    },

    # Chennai
    {
        "hotel_id": 1011,
        "hotel_name": "Taj Coromandel",
        "city_id": 5,
        "hotel_rating": 5,
        "price_per_night": 11200
    },
    {
        "hotel_id": 1012,
        "hotel_name": "The Park Chennai",
        "city_id": 5,
        "hotel_rating": 4,
        "price_per_night": 7900
    },

    # Kolkata
    {
        "hotel_id": 1013,
        "hotel_name": "ITC Royal Bengal",
        "city_id": 6,
        "hotel_rating": 5,
        "price_per_night": 10800
    },
    {
        "hotel_id": 1014,
        "hotel_name": "The Lalit Kolkata",
        "city_id": 6,
        "hotel_rating": 5,
        "price_per_night": 9900
    },

    # Ahmedabad
    {
        "hotel_id": 1015,
        "hotel_name": "Hyatt Ahmedabad",
        "city_id": 7,
        "hotel_rating": 5,
        "price_per_night": 9100
    },
    {
        "hotel_id": 1016,
        "hotel_name": "Novotel Ahmedabad",
        "city_id": 7,
        "hotel_rating": 4,
        "price_per_night": 6500
    },

    # Jaipur
    {
        "hotel_id": 1017,
        "hotel_name": "Rambagh Palace",
        "city_id": 8,
        "hotel_rating": 5,
        "price_per_night": 24000
    },
    {
        "hotel_id": 1018,
        "hotel_name": "Hilton Jaipur",
        "city_id": 8,
        "hotel_rating": 5,
        "price_per_night": 8700
    },

    # Goa
    {
        "hotel_id": 1019,
        "hotel_name": "Taj Fort Aguada",
        "city_id": 9,
        "hotel_rating": 5,
        "price_per_night": 17800
    },
    {
        "hotel_id": 1020,
        "hotel_name": "W Goa",
        "city_id": 9,
        "hotel_rating": 5,
        "price_per_night": 19800
    },

    # Pune
    {
        "hotel_id": 1021,
        "hotel_name": "JW Marriott Pune",
        "city_id": 10,
        "hotel_rating": 5,
        "price_per_night": 11800
    },
    {
        "hotel_id": 1022,
        "hotel_name": "Conrad Pune",
        "city_id": 10,
        "hotel_rating": 5,
        "price_per_night": 10900
    },

    # Lucknow
    {
        "hotel_id": 1023,
        "hotel_name": "Taj Mahal Lucknow",
        "city_id": 11,
        "hotel_rating": 5,
        "price_per_night": 9300
    },
    {
        "hotel_id": 1024,
        "hotel_name": "Renaissance Lucknow",
        "city_id": 11,
        "hotel_rating": 5,
        "price_per_night": 8800
    },

    # Chandigarh
    {
        "hotel_id": 1025,
        "hotel_name": "JW Marriott Chandigarh",
        "city_id": 12,
        "hotel_rating": 5,
        "price_per_night": 9700
    },
    {
        "hotel_id": 1026,
        "hotel_name": "Hyatt Regency Chandigarh",
        "city_id": 12,
        "hotel_rating": 5,
        "price_per_night": 9200
    },

    # Varanasi
    {
        "hotel_id": 1027,
        "hotel_name": "Taj Ganges",
        "city_id": 13,
        "hotel_rating": 5,
        "price_per_night": 8400
    },

    # Kochi
    {
        "hotel_id": 1028,
        "hotel_name": "Grand Hyatt Kochi",
        "city_id": 14,
        "hotel_rating": 5,
        "price_per_night": 11500
    },

    # Amritsar
    {
        "hotel_id": 1029,
        "hotel_name": "Hyatt Regency Amritsar",
        "city_id": 15,
        "hotel_rating": 5,
        "price_per_night": 7600
    },

    # Srinagar
    {
        "hotel_id": 1030,
        "hotel_name": "Vivanta Dal View",
        "city_id": 16,
        "hotel_rating": 5,
        "price_per_night": 14200
    },

    # Leh
    {
        "hotel_id": 1031,
        "hotel_name": "The Grand Dragon",
        "city_id": 17,
        "hotel_rating": 5,
        "price_per_night": 9800
    },

    # Port Blair
    {
        "hotel_id": 1032,
        "hotel_name": "SeaShell Resort",
        "city_id": 18,
        "hotel_rating": 5,
        "price_per_night": 12600
    },

    # Udaipur
    {
        "hotel_id": 1033,
        "hotel_name": "The Oberoi Udaivilas",
        "city_id": 19,
        "hotel_rating": 5,
        "price_per_night": 28500
    },

    # Bhubaneswar
    {
        "hotel_id": 1034,
        "hotel_name": "Mayfair Lagoon",
        "city_id": 20,
        "hotel_rating": 5,
        "price_per_night": 9100
    }

]