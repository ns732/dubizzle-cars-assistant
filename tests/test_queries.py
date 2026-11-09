
test_queries = [
    # Specific car searches
    {
        "query": "Find me a Toyota",
        "expected_make": "toyota",
    },
    {
        "query": "Show me a BMW M4",
        "expected_make": "bmw",
        "expected_model": "m4",
    },
    {
        "query": "Find a Mercedes-Benz GLE",
        "expected_make": "mercedes-benz",
        "expected_model": "gle-class",
    },
    {
        "query": "Show me a Haval H9",
        "expected_make": "haval",
        "expected_model": "h9",
    },
    {
        "query": "Find a Range Rover",
        "expected_make": "land rover",
    },
    {
        "query": "Show me a Ford Explorer",
        "expected_make": "ford",
        "expected_model": "explorer",
    },

    # Year-based searches
    {
        "query": "Find a car from 2025",
        "expected_year": 2025,
    },
    {
        "query": "Show me a 2023 Nissan Patrol",
        "expected_make": "nissan",
        "expected_model": "patrol",
        "expected_year": 2023,
    },

    # Multiple requirements
    {
        "query": "Find a 2021 BMW M4",
        "expected_make": "bmw",
        "expected_model": "m4",
        "expected_year": 2021,
        "expected_match": False,
    },
    {
        "query": "Find a 2024 Mercedes-Benz C-Class",
        "expected_make": "mercedes-benz",
        "expected_model": "c-class",
        "expected_year": 2024,
    },

    # Description-based searches
    {
        "query": "Find an SUV suitable for family trips",
        "manual_review": True,
    },
    {
        "query": "Find a car for daily commuting",
        "manual_review": True,
    },
    {
        "query": "Show me a luxury car",
        "manual_review": True,
    },

    # Price and mileage searches
    {
        "query": "Find cars under AED 100000",
        "manual_review": True,
    },
    {
        "query": "Show me cars with less than 50000 km",
        "manual_review": True,
    },

    # Cars not present in the dataset
    {
        "query": "Find me a Lamborghini Urus",
        "expected_make": "lamborghini",
        "expected_model": "urus",
        "expected_match": False,
    },
    {
        "query": "Show me a 2022 Porsche 911",
        "expected_make": "porsche",
        "expected_model": "911",
        "expected_year": 2022,
        "expected_match": False,
    },
]
