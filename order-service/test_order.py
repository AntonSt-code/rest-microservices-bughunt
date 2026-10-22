from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient
from main import app, ORDERS

# Створюємо клієнт для тестування Order Service
client = TestClient(app)


# Перевіряємо створення замовлення без токена
def test_create_order_without_token():

    # Запам'ятовуємо початкову кількість замовлень
    initial_count = len(ORDERS)

    # Імітуємо відмову Auth Service в авторизації
    with patch("main.httpx.AsyncClient") as mock_client:
        mock_auth = mock_client.return_value.__aenter__.return_value

        mock_auth.get = AsyncMock(
            return_value=httpx.Response(
                401,
                json={"error": "missing or invalid token"}
            )
        )

        # Надсилаємо запит без токена
        response = client.post(
            "/orders",
            json={"productId": 100, "qty": 1}
        )

    # Очікуємо HTTP 401 Unauthorized
    assert response.status_code == 401, (
        f"Очікувався статус 401, "
        f"але отримано {response.status_code}"
    )

    # Замовлення не повинно бути створене
    assert len(ORDERS) == initial_count


# Перевірка створення замовлення з авторизацією
def test_create_order_with_token():

    # Запам'ятовуємо початкову кількість замовлень
    initial_count = len(ORDERS)

    # Імітуємо успішну авторизацію
    with patch("main.httpx.AsyncClient") as mock_client:
        mock_auth = mock_client.return_value.__aenter__.return_value

        mock_auth.get = AsyncMock(
            return_value=httpx.Response(
                200,
                json={"email": "alice@example.com"}
            )
        )

        try:
            # Надсилаємо запит з навчальним токеном
            response = client.post(
                "/orders",
                json={"productId": 100, "qty": 1},
                headers={
                    "Authorization": "Bearer fake-token-for-alice@example.com"
                }
            )

            # Очікуємо успішне створення замовлення
            assert response.status_code == 201

            # Перевіряємо кількість замовлень
            assert len(ORDERS) == initial_count + 1

            # Перевіряємо отримані дані
            order = response.json()

            assert order["product_id"] == 100
            assert order["quantity"] == 1
            assert order["status"] == "created"

        finally:
            # Прибираємо тестове замовлення
            del ORDERS[initial_count:]