
from app.services.inventory import InventoryLoader

inventory = InventoryLoader().load_inventory()

targets = [
    ("mercedes-benz", "v-class"),
    ("byd", "han"),
    ("audi", "q8"),
    ("bmw", "i4"),
    ("land rover", "range rover evoque"),
]

for make, model in targets:
    matches = inventory[
        (inventory["make_normalized"] == make) &
        (inventory["model_normalized"] == model)
    ]

    for _, car in matches.iterrows():
        print("\n" + "=" * 70)
        print(f"{car['make']} {car['model']} ({car['year']})")
        print("TITLE:", car["title"])
        print("DESCRIPTION:")
        print(car["clean_description"])
