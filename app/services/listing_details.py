import re


class ListingDetails:

    AMOUNT = r"(\d{1,3}(?:[,\s]\d{3})+|\d+)(?:\.\d{1,2})?"

    PRICE_PATTERN = re.compile(
        rf"(?:AED|Dhs?\.?)\s*{AMOUNT}"
        rf"|{AMOUNT}\s*(?:AED|Dhs?\.?)",
        re.IGNORECASE
    )

    @staticmethod
    def _number(value):
        return float(re.sub(r"[,\s]", "", value))

    @classmethod
    def extract_price(cls, text):
        text = str(text or "")

        if re.search(r"salary\s+requirement", text, re.IGNORECASE):
            return None

        amount = cls.AMOUNT

        labelled_patterns = [
            rf"(?:selling\s+price|cash\s+price|price)"
            rf"\s*[:\-]?\s*(?:AED|Dhs?\.?)?\s*{amount}",
            rf"(?:AED|Dhs?\.?)\s*{amount}\s*(?:cash|in\s+cash)\b",
            rf"{amount}\s*(?:AED|Dhs?\.?)?\s*(?:cash\s+price|selling\s+price)",
        ]

        for pattern in labelled_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = re.search(amount, match.group(0))
                if value:
                    return cls._number(value.group(1))

        candidates = []

        for match in cls.PRICE_PATTERN.finditer(text):
            raw = match.group(1) or match.group(2)
            value = cls._number(raw)

            before = text[max(0, match.start() - 45):match.start()]
            after = text[match.end():min(len(text), match.end() + 55)]

            if re.search(
                r"down[\s-]*payment|deposit|monthly|per\s+month|"
                r"installments?|instalments?",
                before[-30:],
                re.IGNORECASE
            ):
                continue

            if re.match(
                r"\s*(?:p\.?\s*m\.?|p/m|/\s*month|per\s+month|"
                r"monthly|installments?|instalments?)\b",
                after,
                re.IGNORECASE
            ):
                continue

            if re.search(
                r"\b(?:monthly|per\s+month|installments?|instalments?)\b",
                before[-30:],
                re.IGNORECASE
            ):
                continue

            if value < 1000:
                continue

            is_cash = bool(re.match(r"\s*(?:cash|in\s+cash)\b", after, re.IGNORECASE))
            is_labelled = bool(
                re.search(r"(?:price|cash price|selling price)\s*[:\-]?\s*$",
                          before, re.IGNORECASE)
            )
            candidates.append((value, is_cash, is_labelled, match.start()))

        if not candidates:
            return None

        preferred = [item for item in candidates if item[1] or item[2]]
        if preferred:
            return preferred[0][0]

        return candidates[0][0]

    @staticmethod
    def extract_mileage(text, title=False):
        text = str(text or "")

        explicit_patterns = [
            r"(?:mileage|odometer)\s*[:\-]?\s*"
            r"([\d,]+)\s*(?:km|kms|kilometres|kilometers)\b",
            r"\b(?:only|brand new\s*[-–—]?\s*only)\s*"
            r"([\d,]+)\s*(?:km|kms)\s*mileage\b"
        ]

        for pattern in explicit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1).replace(",", ""))

        range_values = {
            int(match.group(1).replace(",", ""))
            for match in re.finditer(
                r"\b([\d,]+)\s*km(?:s)?\s+(?:driving\s+)?range\b",
                text,
                re.IGNORECASE
            )
        }

        text = re.sub(
            r"(?:last|next)\s+service\s*:\s*"
            r"[\d,]+\s*km(?:\s*\([^)]*\))?",
            "",
            text,
            flags=re.IGNORECASE
        )

        vehicle_specs = re.search(
            r"VEHICLE\s+SPECS\s*[:\-]?\s*(.*?)(?:OPTIONS\s*&\s*FEATURES|CONTACT|$)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if vehicle_specs:
            for match in re.finditer(
                r"\b([\d,]+)\s*(?:km|kms|kilometres|kilometers)\b",
                vehicle_specs.group(1),
                re.IGNORECASE
            ):
                value = int(match.group(1).replace(",", ""))
                if value not in range_values:
                    return value

        pattern = r"\b([\d,]+)\s*(?:km|kms|kilometres|kilometers)\b"
        excluded_terms = (
            r"warranty|service contract|service plan|"
            r"driving range|electric range|battery range|"
            r"range on a single charge|\brange\b|"
            r"top speed|last service|next service"
        )

        for match in re.finditer(pattern, text, re.IGNORECASE):
            value = int(match.group(1).replace(",", ""))

            if value in range_values:
                continue

            before = text[max(0, match.start() - 80):match.start()]
            after = text[match.end():match.end() + 80]

            if re.search(excluded_terms, before + after, re.IGNORECASE):
                continue

            return value

        if title:
            match = re.search(r"\b([\d,]+)\s*kms?\b", text, re.IGNORECASE)
            if match:
                value = int(match.group(1).replace(",", ""))
                if value == 0 or re.search(r"\bonly\b", text[match.end():], re.IGNORECASE):
                    return value

        return None

    @classmethod
    def extract_details(cls, title, description):
        title = str(title or "")
        description = str(description or "")
        price = cls.extract_price(f"{title}\n{description}")
        mileage = cls.extract_mileage(description)

        if mileage is None:
            title_mileage = cls.extract_mileage(title, title=True)
            range_values = {
                int(match.group(1).replace(",", ""))
                for match in re.finditer(
                    r"\b([\d,]+)\s*km(?:s)?\s+(?:driving\s+)?range\b",
                    description,
                    re.IGNORECASE
                )
            }
            if title_mileage not in range_values:
                mileage = title_mileage

        return {"price_aed": price, "mileage_km": mileage}


if __name__ == "__main__":
    from app.services.inventory import InventoryLoader

    inventory = InventoryLoader().load_inventory()
    for _, car in inventory.iterrows():
        details = ListingDetails.extract_details(
            car["title"], car["clean_description"]
        )
        print(
            f"{car['make']} {car['model']} ({car['year']}) | "
            f"Price: {details['price_aed']} | Mileage: {details['mileage_km']}"
        )
