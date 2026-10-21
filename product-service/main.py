from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Створюємо застосунок каталогу товарів
app = FastAPI(title="ProductService")

# Навчальний каталог товарів
PRODUCTS = [
    {
        "product_id": 100,
        "name": "Keyboard",
        "price": "59.99",
        "inStock": 5
    },
    {
        "product_id": 101,
        "name": "Mouse",
        "price": "29.99",
        "inStock": 0
    }
]


# Отримання списку всіх товарів
@app.get("/products")
async def list_products():
    return {"items": PRODUCTS}


# Отримання товару за його ідентифікатором
@app.get("/products/{pid}")
async def get_product(pid: int):

    for product in PRODUCTS:
        if product["product_id"] == pid:
            return product

    # Повертаємо 404, якщо товар не знайдено
    return JSONResponse(
        {"message": "not found"},
        status_code=404
    )
