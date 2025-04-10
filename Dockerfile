FROM python:3.12-slim

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем рабочую директорию
WORKDIR /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Копируем pyproject и README
COPY pyproject.toml poetry.lock README.md /app/

# Копируем весь src (раньше!)
COPY ./src /app/src

# Показываем, что скопировалось (отладка)
RUN ls -la /app/src/first_project_django

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Переходим в рабочую директорию
WORKDIR /app/src

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
