# Dockerfile


FROM python:3.12-slim


WORKDIR /app

# Копируем файлы requirements и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY exchange ./exchange


# # Команда для запуска приложения
# CMD ["python3", "exchange.manage.py", "migrate"]
# CMD ["python3", "exchange.manage.py", "runserver"]

