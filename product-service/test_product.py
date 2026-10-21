from fastapi.testclient import TestClient
from main import app

# Створюємо тестовий клієнт Product Service
client = TestClient(app)


# Перевірка отримання неіснуючого товару
def test_product_not_found():

    # Надсилаємо запит із неіснуючим ID товару
    response = client.get("/products/999")

    # Очікуємо HTTP 404 Not Found
    assert response.status_code == 404, (
        f"Очікувався статус 404, "
        f"але отримано {response.status_code}"
    )


# Перевірка отримання існуючого товару
def test_product_exists():

    # Надсилаємо запит до товару з ID 100
    response = client.get("/products/100")

    # Очікуємо успішний HTTP-статус 200
    assert response.status_code == 200

    # Перевіряємо правильність ID товару
    product = response.json()
    assert product["product_id"] == 100