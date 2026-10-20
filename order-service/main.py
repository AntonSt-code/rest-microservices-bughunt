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

    # Намагаємося перевірити токен користувача
    async with httpx.AsyncClient() as client:
        _ = await client.get(
            f"{AUTH_URL}/whoami",
            headers={"Authorization": authorization or ""}
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