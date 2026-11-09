
from app.services.inventory import InventoryLoader

inventory = InventoryLoader().load_inventory()

missing_prices = inventory[inventory["price_aed"].isna()]
missing_mileage = inventory[inventory["mileage_km"].isna()]

print("\nLISTINGS WITHOUT EXTRACTED PRICES")
print("=" * 60)

for _, car in missing_prices.head(15).iterrows():
    print(f"\n{car['make']} {car['model']} ({car['year']})")
    print("Title:", car["title"])
    print("Description:", car["clean_description"][:500])


print("\nLISTINGS WITHOUT EXTRACTED MILEAGE")
print("=" * 60)

for _, car in missing_mileage.head(10).iterrows():
    print(f"\n{car['make']} {car['model']} ({car['year']})")
    print("Description:", car["clean_description"][:300])
