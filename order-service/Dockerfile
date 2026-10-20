# Використовуємо Python 3.11
FROM python:3.11-slim

# Робоча папка всередині контейнера
WORKDIR /app

# Копіюємо список бібліотек
COPY requirements.txt ./

# Встановлюємо необхідні бібліотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код сервісу
COPY main.py ./

# Порт, який використовує сервіс
EXPOSE 8000

# Запускаємо FastAPI через Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]