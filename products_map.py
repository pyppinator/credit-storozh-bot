from products import BANKS

PRODUCTS_MAP = {}

def _add_product(bank_name, prod_data):
    key = (bank_name, prod_data["name"])
    PRODUCTS_MAP[key] = (
        prod_data["url"],
        prod_data["selector"],
        prod_data.get("action"),
        prod_data.get("column_index")
    )

for bank_id, bank_data in BANKS.items():
    bank_name = bank_data["name"]

    # Обычные продукты
    if "products" in bank_data:
        for prod_id, prod_data in bank_data["products"].items():
            _add_product(bank_name, prod_data)

    # Продукты в группах (без категорий)
    if "groups" in bank_data:
        for group_id, group_data in bank_data["groups"].items():
            for prod_id, prod_data in group_data["products"].items():
                _add_product(bank_name, prod_data)

    # Продукты в категориях → группах
    if "categories" in bank_data:
        for cat_id, cat_data in bank_data["categories"].items():
            for group_id, group_data in cat_data["groups"].items():
                for prod_id, prod_data in group_data["products"].items():
                    _add_product(bank_name, prod_data)