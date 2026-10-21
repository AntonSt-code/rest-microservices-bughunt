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


# Перевірка отримання токена з HTTP-заголовка
def test_whoami_authorization_header():

    # Передаємо токен через заголовок Authorization
    response = client.get(
        "/whoami",
        headers={
            "Authorization": "Bearer fake-token-for-alice@example.com"
        }
    )

    # Перевіряємо, чи сервер прийняв заголовок
    assert response.status_code == 200, (
        f"Очікувався статус 200, "
        f"але отримано {response.status_code}"
    )


# Перевірка правильності адреси після обробки Bearer
def test_whoami_email_without_extra_spaces():

    # Передаємо навчальний токен через HTTP-заголовок
    response = client.get(
        "/whoami",
        headers={
            "Authorization": "Bearer fake-token-for-alice@example.com"
        }
    )

    # Перевіряємо успішність запиту
    assert response.status_code == 200

    # Отримуємо електронну адресу з JSON-відповіді
    email = response.json()["email"]

    # Перевіряємо відсутність зайвих пробілів
    assert email == "alice@example.com", (
        f"Очікувалася адреса 'alice@example.com', "
        f"але отримано '{email}'"
    )