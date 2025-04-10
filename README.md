Hotel Room Booking Service

Простой Django-сервис для управления номерами отеля и бронированиями.

✨ Возможности

🏨 Каталог номеров:
- ✅ Добавление номера отеля
- ❌ Удаление номера (+ все брони)
- 📅 Список номеров c сортировкой (по цене, дате)

🛌 Бронирования:
- ✅ Добавление брони (с проверкой на пересечение дат)
- ❌ Удаление брони
- 🔍 Список броней для номера отсортированных по дате начала

---

🚀 Запуск через Docker

1. Сборка и запуск
```bash
docker compose down -v
docker compose up --build
```

2. Миграции
```bash
docker compose exec web python manage.py migrate
```

3. Создание суперюзера (admin)
```bash
docker compose exec web python manage.py createsuperuser
```

4. Открыть в браузере:

- Сайт: [http://localhost:8000](http://localhost:8000)
- Админка: [http://localhost:8000/admin](http://localhost:8000/admin)

---

🔢 Примеры API-запросов

✅ Создание брони:
```bash
curl -X POST \
     -d "room_id=24" \
     -d "date_start=2025-06-01" \
     -d "date_end=2025-06-05" \
     http://localhost:8000/bookings/create
```
Ответ:
```json
{"booking_id": 1444}
```

 🔍 Список броней:
```bash
curl -X GET "http://localhost:8000/bookings/list?room_id=24"
```
Ответ:
```json
[
  {"booking_id": 1444, "date_start": "2025-06-01", "date_end": "2025-06-05"},
  ...
]
```

---

 🐞 Тестирование

Запуск юнит-тестов:
```bash
docker compose exec web pytest rooms_app/tests.py

```

---

🎓 Зависимости

- Python 3.12
- Django 5.2
- PostgreSQL 15
- Poetry
- Docker & Docker Compose
- Ruff, Pre-commit, Pytest

---

🌟 TODO

- [x] Перенос проекта в Docker
- [x] API-хендлеры для CRUD
- [x] Проверка пересечения дат брони
- [x] Тесты

---

