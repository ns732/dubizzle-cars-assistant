
from app.services.query_understanding import QueryUnderstanding
from app.services.retrieval import CarRetriever


class CarSearchService:

    def __init__(self):
        self.query_understanding = QueryUnderstanding()
        self.retriever = CarRetriever()

    def search(self, message, conversation_history=None, limit=100):
        requirements = self.query_understanding.understand(
            message,
            conversation_history
        )

        if requirements["intent"] != "search_cars":
            return {
                "intent": requirements["intent"],
                "requirements": requirements,
                "cars": [],
                "message": requirements.get("clarification_question")
            }

        if requirements.get("clarification_needed"):
            return {
                "intent": "search_cars",
                "requirements": requirements,
                "cars": [],
                "message": requirements.get("clarification_question")
            }

        cars = self.retriever.search(
            query=message,
            make=requirements.get("make"),
            model=requirements.get("model"),
            min_year=requirements.get("min_year"),
            max_year=requirements.get("max_year"),
            min_price=requirements.get("min_price"),
            max_price=requirements.get("max_price"),
            min_mileage=requirements.get("min_mileage"),
            max_mileage=requirements.get("max_mileage"),
            body_type=requirements.get("body_type"),
            fuel_type=requirements.get("fuel_type"),
            transmission=requirements.get("transmission"),
            limit=limit
        )

        return {
            "intent": "search_cars",
            "requirements": requirements,
            "cars": cars,
            "message": (
                f"Found {len(cars)} matching cars."
                if cars else
                "I couldn't find cars matching all those requirements."
            )
        }


if __name__ == "__main__":
    service = CarSearchService()

    result = service.search(
        "Find me a Toyota SUV under AED 100,000, from 2022 onwards, with less than 50,000 km"
    )

    print("\nSearch requirements:")
    print(result["requirements"])

    print("\nSearch result:")
    print(result["message"])

    for car in result["cars"]:
        print(
            f"{car['make']} {car['model']} ({car['year']}) | "
            f"Price: {car['price_aed']} | "
            f"Mileage: {car['mileage_km']}"
        )
