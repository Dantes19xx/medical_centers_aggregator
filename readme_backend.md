# Medical Centers Aggregator — Backend

REST API для агрегатора медицинских учреждений Алматы.

---

## Быстрый старт — Docker Compose (рекомендуется)

### Требования
- Docker >= 24
- Docker Compose >= 2.x

### 1. Скопировать .env файл

```bash
cd backend
cp .env.example .env
```

При необходимости отредактируйте пароли в `.env`.

### 2. Запустить

```bash
cd backend
docker compose up --build
```

Это запустит PostgreSQL, применит миграции (`alembic upgrade head`) и поднимет API на порту **8000**.

### 3. Заполнить тестовыми данными

```bash
docker compose exec app python seed.py
```

### 4. Открыть документацию

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

---

## Запуск локально (без Docker)

### Требования
- Python 3.11+
- PostgreSQL (запущенный локально)

### 1. Создать виртуальное окружение

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Настроить .env

```bash
cp .env.example .env
# Отредактировать DATABASE_URL под вашу БД
```

Создать базу данных вручную:

```sql
CREATE DATABASE medical_db;
CREATE USER medical_user WITH PASSWORD 'medical_password';
GRANT ALL PRIVILEGES ON DATABASE medical_db TO medical_user;
```

### 4. Применить миграции

```bash
alembic upgrade head
```

### 5. Заполнить тестовыми данными

```bash
python seed.py
```

### 6. Запустить сервер

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Тестовые учётные данные

| Роль | Email | Пароль |
|------|-------|--------|
| Администратор | admin@medical.kz | admin123 |
| Пациент 1 | asel.nurova@mail.ru | password123 |
| Пациент 2 | damir.seitkali@mail.ru | password123 |

---

## Основные эндпоинты

```
GET  /health                          — проверка работоспособности
GET  /docs                            — Swagger UI

POST /api/v1/auth/register            — регистрация
POST /api/v1/auth/login               — вход (возвращает JWT)
GET  /api/v1/auth/me                  — текущий пользователь

GET  /api/v1/clinics                  — список клиник
GET  /api/v1/clinics/{id}             — страница клиники
GET  /api/v1/doctors                  — список врачей
GET  /api/v1/doctors/{id}/slots       — свободные слоты
GET  /api/v1/services                 — услуги
POST /api/v1/appointments             — запись к врачу
POST /api/v1/reviews                  — оставить отзыв
POST /api/v1/chatbot/message          — чат-бот
```

---

## Структура проекта

```
backend/
├── app/
│   ├── main.py          — точка входа FastAPI
│   ├── config.py        — настройки (pydantic-settings)
│   ├── database.py      — SQLAlchemy сессия
│   ├── models/          — ORM модели
│   ├── schemas/         — Pydantic v2 схемы
│   ├── crud/            — операции с БД
│   ├── routers/         — маршруты API
│   └── utils/           — JWT, пагинация
├── alembic/             — миграции
├── seed.py              — тестовые данные
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```
