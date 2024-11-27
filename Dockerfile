# Используем официальный образ Python версии 3.10
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем необходимые библиотеки из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
