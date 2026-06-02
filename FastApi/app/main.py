from fastapi import FastAPI

app = FastAPI()

# static route

@app.get("/")

def root():
    return {"message": "Hello, World!"}

# dynamic route

@app.get("/products/{id}")
def get_product(id: int):
    products = ["Laptop", "Smartphone", "Tablet" , "Headphones", "Smartwatch"]
    if id < 0 or id >= len(products):
        return {"error": "Product not found"}

    return products[id]