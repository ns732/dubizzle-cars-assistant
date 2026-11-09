
import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


class QueryUnderstanding:
    def __init__(self):
        self.client = client
        self.model = GROQ_MODEL

    def understand(self, message, conversation_history=None):
        """
        Extract structured requirements using Groq.
        If the API is unavailable, use local rule-based understanding.
        """
        if self.client:
            try:
                return self._groq_understand(message, conversation_history)
            except Exception as error:
                print(f"Groq unavailable; using local fallback. Reason: {error}")

        return self._local_understand(message, conversation_history)

    def _groq_understand(self, message, conversation_history=None):
        history = conversation_history or []

        prompt = f"""
You are the query-understanding component of a used-car marketplace assistant
for dubizzle in the UAE.

Analyse the latest user message using the conversation history.

Return ONLY one valid JSON object. Do not use Markdown.

The JSON must contain exactly these fields:
{{
    "intent": "search_cars",
    "make": null,
    "model": null,
    "min_year": null,
    "max_year": null,
    "min_price": null,
    "max_price": null,
    "min_mileage": null,
    "max_mileage": null,
    "body_type": null,
    "fuel_type": null,
    "transmission": null,
    "keywords": [],
    "clarification_needed": false,
    "clarification_question": null
}}

Intent must be one of:
- search_cars: user wants to find, browse, or compare available cars.
- car_details: user asks about a previously shown car or listing.
- general_car_question: user asks a general automotive question.
- chit_chat: greetings or casual conversation.
- out_of_scope: unrelated non-automotive requests.

Rules:
1. Extract only requirements explicitly stated or clearly established in context.
2. Do not invent missing filters.
3. Convert AED amounts to numbers. For example, AED 100,000 becomes 100000.
4. Convert mileage to kilometres.
5. "Under", "below", or "less than" means a maximum.
6. "Above", "over", or "from" means a minimum.
7. "From 2022 onwards" means min_year = 2022.
8. Recognise SUV, sedan, hatchback, coupe, convertible, pickup and van.
9. Preserve the distinction between monthly instalments and total selling price.
10. A follow-up about warranty, features, or specifications of a previously
    displayed car should be car_details.
11. If the user says "first car", "second one", or similar, use car_details.
12. If the user asks for cars but a critical requirement is ambiguous,
    set clarification_needed to true and provide one short question.
13. Never claim that a car exists in inventory. This component only extracts intent.

Conversation history:
{json.dumps(history[-10:], ensure_ascii=False, default=str)}

Latest user message:
{message}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You extract structured automotive search requirements. Return valid JSON only."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=700
        )

        content = response.choices[0].message.content.strip()

        # Remove Markdown code fences if the model includes them.
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        result = json.loads(content)
        return self._normalise_result(result)

    def _local_understand(self, message, conversation_history=None):
        """
        Basic rule-based fallback.
        Keeps core search filters working without an external API.
        """
        text = message.lower()

        result = {
            "intent": "out_of_scope",
            "make": None,
            "model": None,
            "min_year": None,
            "max_year": None,
            "min_price": None,
            "max_price": None,
            "min_mileage": None,
            "max_mileage": None,
            "body_type": None,
            "fuel_type": None,
            "transmission": None,
            "keywords": [],
            "clarification_needed": False,
            "clarification_question": None
        }

        greetings = [
            "hi", "hello", "hey", "good morning",
            "good afternoon", "good evening", "thanks", "thank you"
        ]

        if text.strip().rstrip("!. ") in greetings:
            result["intent"] = "chit_chat"
            return result

        detail_terms = [
            "warranty", "mileage", "specification", "specifications",
            "features", "engine", "service history", "does it have",
            "is it available", "tell me about", "what about the first",
            "what about the second", "first car", "second car"
        ]

        if any(term in text for term in detail_terms):
            result["intent"] = "car_details"
            return result

        automotive_terms = [
            "car", "vehicle", "engine", "tyre", "tire", "brake",
            "insurance", "registration", "maintenance", "fuel",
            "transmission", "hybrid", "electric vehicle", "ev"
        ]

        search_terms = [
            "find", "search", "show", "looking for", "recommend",
            "options", "listings", "available cars", "buy"
        ]

        if any(term in text for term in search_terms):
            result["intent"] = "search_cars"
        elif any(term in text for term in automotive_terms):
            result["intent"] = "general_car_question"
            return result
        else:
            return result

        # Make extraction
        makes = [
            "toyota", "nissan", "honda", "hyundai", "kia",
            "ford", "bmw", "mercedes-benz", "mercedes",
            "audi", "lexus", "tesla", "byd", "haval",
            "volkswagen", "land rover", "range rover",
            "chevrolet", "mazda", "mitsubishi", "jeep",
            "porsche", "volvo", "infiniti", "renault"
        ]

        for make in sorted(makes, key=len, reverse=True):
            if re.search(r"\b" + re.escape(make) + r"\b", text):
                result["make"] = make
                break

        # Year filters
        years = [int(y) for y in re.findall(r"\b20(?:1[5-9]|2[0-9])\b", text)]

        if years:
            if any(term in text for term in ["onwards", "and newer", "or newer", "from"]):
                result["min_year"] = min(years)
            elif any(term in text for term in ["before", "older than", "until"]):
                result["max_year"] = max(years)
            elif len(years) >= 2:
                result["min_year"] = min(years)
                result["max_year"] = max(years)
            else:
                result["min_year"] = years[0]
                result["max_year"] = years[0]

        # Price extraction: AED values only, avoiding monthly amounts.
        price_match = re.search(
            r"(?:aed|dhs?)\s*([\d,]+(?:\.\d+)?)",
            text
        )

        if price_match:
            amount = float(price_match.group(1).replace(",", ""))
            if any(term in text for term in ["under", "below", "less than", "maximum", "max"]):
                result["max_price"] = amount
            elif any(term in text for term in ["above", "over", "more than", "minimum", "min"]):
                result["min_price"] = amount

        # Mileage extraction
        mileage_match = re.search(
            r"([\d,]+)\s*(?:km|kms|kilometres|kilometers)",
            text
        )

        if mileage_match:
            mileage = float(mileage_match.group(1).replace(",", ""))
            if any(term in text for term in ["under", "below", "less than", "maximum", "max"]):
                result["max_mileage"] = mileage
            elif any(term in text for term in ["above", "over", "more than", "minimum", "min"]):
                result["min_mileage"] = mileage

        # Body type
        for body_type in [
            "suv", "sedan", "hatchback", "coupe",
            "convertible", "pickup", "van"
        ]:
            if body_type in text:
                result["body_type"] = body_type.upper()
                break

        # Fuel type
        for fuel in ["petrol", "diesel", "hybrid", "electric"]:
            if fuel in text:
                result["fuel_type"] = fuel
                break

        # Transmission
        for transmission in ["automatic", "manual"]:
            if transmission in text:
                result["transmission"] = transmission
                break

        return result

    @staticmethod
    def _normalise_result(result):
        fields = {
            "intent": "out_of_scope",
            "make": None,
            "model": None,
            "min_year": None,
            "max_year": None,
            "min_price": None,
            "max_price": None,
            "min_mileage": None,
            "max_mileage": None,
            "body_type": None,
            "fuel_type": None,
            "transmission": None,
            "keywords": [],
            "clarification_needed": False,
            "clarification_question": None
        }

        for key in fields:
            if key in result:
                fields[key] = result[key]

        valid_intents = {
            "search_cars",
            "car_details",
            "general_car_question",
            "chit_chat",
            "out_of_scope"
        }

        if fields["intent"] not in valid_intents:
            fields["intent"] = "out_of_scope"

        if not isinstance(fields["keywords"], list):
            fields["keywords"] = []

        return fields
