from fastapi.testclient import TestClient
from main import app

# Створюємо тестовий клієнт Auth Service
client = TestClient(app)


# Перевіряємо неправильний пароль користувача
def test_login_invalid_password():

    # Надсилаємо запит із неправильним паролем
    response = client.get(
        "/login",
        params={
            "email": "alice@example.com",
            "password": "wrongpassword"
        }
    )

    # Очікуємо HTTP 401 Unauthorized
    assert response.status_code == 401, (
        f"Очікувався статус 401, "
        f"але отримано {response.status_code}"
    )