from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from app.services.products import get_all_products, get_product_by_id

app = FastAPI(
    title="Products API",
    version="1.0.0",
    description="Product Catalog API"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to FastAPI Product Service"
    }


@app.get("/products")
def list_products(
    name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="Filter products by name"
    ),
    sort_by_price: bool = Query(
        default=False,
        description="Sort products by price"
    ),
    order: str = Query(
        default="asc",
        pattern="^(asc|desc)$",
        description="Sort order: asc or desc"
    )
):
    products = get_all_products()

    # Filter by name
    if name:
        products = [
            p for p in products
            if name.lower() in p.get("name", "").lower()
        ]

        if not products:
            raise HTTPException(
                status_code=404,
                detail="No products found matching the filter"
            )

    # Sort by price
    if sort_by_price:
        products = sorted(
            products,
            key=lambda p: p.get("price", 0),
            reverse=(order == "desc")
        )

    return {
        "total": len(products),
        "products": products
    }


@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@app.post("/products" , status_code=201)
def create_product(product):
    return product