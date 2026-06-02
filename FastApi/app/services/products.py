import json
from pathlib import Path


def _data_path():

  
    return Path(__file__).parent.parent / "data" / "products.json"
def get_all_products():
    path = _data_path()

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def get_product_by_id(product_id):
    products = get_all_products()

    for product in products:
        if (
            str(product.get("id")) == str(product_id)
            or str(product.get("sku")) == str(product_id)
        ):
            return product

    return None