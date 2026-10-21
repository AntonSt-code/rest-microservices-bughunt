from fastapi import FastAPI, Response, Header
from fastapi.responses import JSONResponse

# Створюємо застосунок авторизації
app = FastAPI(title="AuthService")

# Навчальне сховище користувачів
USERS = {
    "alice@example.com": {"password": "alice123", "id": 1},
    "bob@example.com": {"password": "bob123", "id": 2},
}


# Авторизація користувача
@app.get("/login")
async def login(email: str, password: str, response: Response):

    user = USERS.get(email)

    # Перевіряємо облікові дані
    if not user or user["password"] != password:
        return JSONResponse(
            {"message": "invalid credentials"},
            status_code=200
        )

    # Спрощений навчальний токен
    token = f"fake-token-for-{email}"

    return {
        "accessToken": token,
        "userId": user["id"]
    }


# Отримання інформації про користувача
@app.get("/whoami")
async def whoami(
    authorization: str | None = Header(default=None)
):


    # Перевіряємо наявність токена
    if not authorization or not authorization.startswith("Bearer"):
        return JSONResponse(
            {"error": "missing or invalid token"},
            status_code=401
        )

    # Отримуємо дані з навчального токена
    token = authorization.removeprefix("Bearer ")
    email = token.replace("fake-token-for-", "")

    return {"email": email}
