import os
import httpx

from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse

# Створюємо застосунок замовлень
app = FastAPI(title="OrderService")

# Адреси інших мікросервісів
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8001")
PRODUCT_URL = os.getenv("PRODUCT_URL", "http://localhost:8002")

# Навчальне сховище замовлень
ORDERS: list[dict] = []


# Створення нового замовлення
@app.post("/orders")
async def create_order(
    payload: dict,
    authorization: str | None = Header(default=None)
):

    # Очікувані дані:
    # {"productId": int, "qty": int}


    # Перевіряємо авторизацію через Auth Service
    async with httpx.AsyncClient() as client:
        auth_response = await client.get(
            f"{AUTH_URL}/whoami",
            headers={"Authorization": authorization or ""}
        )

    # Забороняємо створення замовлення без авторизації
    if auth_response.status_code == 401:
        return JSONResponse(
            {"message": "unauthorized"},
            status_code=401
        )

    # Інші помилки Auth Service теж не дозволяють створити замовлення
    if auth_response.status_code != 200:
        return JSONResponse(
            {"message": "authentication service error"},
            status_code=502
        )

    # Створюємо замовлення
    order = {
        "order_id": len(ORDERS) + 1,
        "product_id": payload.get("productId"),
        "quantity": payload.get("qty"),
        "status": "created"
    }

    # Зберігаємо замовлення
    ORDERS.append(order)

    return JSONResponse(order, status_code=201)


# Отримання списку замовлень
@app.get("/orders")
async def list_orders():
    return {"orders": ORDERS}