from fastapi.testclient import TestClient
from main import app

# Створюємо клієнт для тестування Auth Service
client = TestClient(app)


# Перевірка відповіді без токена авторизації
def test_whoami_without_token():

    # Надсилаємо запит без токена
    response = client.get("/whoami")

    # Очікуємо помилку авторизації 401
    assert response.status_code == 401, (
        f"Очікувався статус 401, "
        f"але отримано {response.status_code}"
    )