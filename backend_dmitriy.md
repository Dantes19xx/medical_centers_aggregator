# Backend Summary — Medical Centers Aggregator

## Что было сделано

Реализован полноценный REST API бэкенд для агрегатора медицинских учреждений Алматы.

---

## Технологии

| Компонент | Технология |
|-----------|-----------|
| Веб-фреймворк | FastAPI 0.111 |
| СУБД | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 (синхронный) |
| Миграции | Alembic 1.13 |
| Валидация | Pydantic v2 |
| Аутентификация | JWT (python-jose), bcrypt/passlib |
| ASGI сервер | Uvicorn |
| Контейнеризация | Docker + Docker Compose |

---

## Структура проекта

```
backend/
├── app/
│   ├── main.py          — точка входа, CORS, логирование, health check
│   ├── config.py        — настройки через pydantic-settings + .env
│   ├── database.py      — SQLAlchemy engine, SessionLocal, get_db()
│   ├── models/          — 6 ORM моделей (UUID PK)
│   ├── schemas/         — Pydantic v2 схемы (in/out/list)
│   ├── crud/            — слой доступа к данным
│   ├── routers/         — 7 роутеров FastAPI
│   └── utils/           — JWT-утилиты, пагинация
├── alembic/             — миграции БД
├── seed.py              — заполнение тестовыми данными
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## База данных — модели

| Модель | Ключевые поля |
|--------|--------------|
| **User** | email, hashed_password, full_name, phone, role (patient/admin) |
| **Clinic** | name, address, city, district, phone, working_hours (JSON), photos (ARRAY), rating |
| **Doctor** | clinic_id (FK), ФИО, specialty, experience_years, consultation_price, rating |
| **Service** | clinic_id (FK), name, category, price_from/price_to, duration_minutes |
| **Appointment** | user_id, doctor_id, clinic_id, service_id, date, time, status (pending/confirmed/cancelled/completed) |
| **Review** | user_id, clinic_id/doctor_id, rating (1-5), comment, is_moderated |

---

## API Endpoints (30 эндпоинтов)

### Auth `/api/v1/auth`
- `POST /register` — регистрация
- `POST /login` — вход, возвращает access + refresh JWT
- `POST /refresh` — обновление токена
- `GET /me` — текущий пользователь

### Clinics `/api/v1/clinics`
- `GET /` — список с фильтрами (city, district, specialty, rating_min, search)
- `GET /{id}` — детальная страница
- `GET /{id}/doctors` — врачи клиники
- `GET /{id}/services` — услуги клиники
- `GET /{id}/reviews` — отзывы
- `POST /`, `PUT /{id}`, `DELETE /{id}` — CRUD (admin only)

### Doctors `/api/v1/doctors`
- `GET /` — список с фильтрами (specialty, clinic_id, city, rating, price_max, search)
- `GET /specialties` — список всех специализаций
- `GET /{id}` — профиль врача
- `GET /{id}/reviews` — отзывы о враче
- `GET /{id}/slots?date=YYYY-MM-DD` — свободные слоты на дату (каждые 30 мин)
- `POST /`, `PUT /{id}` — CRUD (admin only)

### Services `/api/v1/services`
- `GET /` — список с фильтрами (clinic_id, category, price_max, search)
- `GET /categories` — список категорий
- `GET /{id}` — детали услуги

### Appointments `/api/v1/appointments`
- `POST /` — создать запись (авторизация необязательна)
- `GET /` — записи текущего пользователя (auth)
- `GET /{id}` — детали записи
- `PATCH /{id}/cancel` — отменить запись

### Reviews `/api/v1/reviews`
- `POST /` — оставить отзыв (auth)
- `GET /` — список с фильтрами (clinic_id, doctor_id)

### Chatbot `/api/v1/chatbot`
- `POST /message` — keyword-based бот, ищет клиники/врачей в БД по ключевым словам

### Health
- `GET /health` — `{"status": "ok", "timestamp": "..."}`

---

## Тестовые данные (seed.py)

- **10 клиник** Алматы (частные и государственные) с районами: Алатауский, Алмалинский, Бостандыкский, Жетысуский, Медеуский, Наурызбайский, Турксибский
- **30+ врачей** по специализациям: терапевт, кардиолог, невролог, педиатр, хирург, офтальмолог, дерматолог, гинеколог, ортопед, стоматолог (цены 3 500–20 000 KZT)
- **55+ услуг** по категориям: Диагностика, Терапия, Хирургия, Педиатрия, Стоматология и др.
- **1 администратор**: `admin@medical.kz` / `admin123`
- **3 пациента** с отзывами

---

## Особенности реализации

- **Пагинация** на всех списочных эндпоинтах: `?page=1&limit=20` → `{items, total, page, limit, pages}`
- **Единый формат ошибок**: `{"detail": "...", "code": "ERROR_CODE"}`
- **CORS**: разрешены `localhost:3000`, `localhost:5173`, `*`
- **JWT**: access token 30 мин, refresh token 7 дней
- **Свободные слоты**: генерируются каждые 30 мин из `working_hours` клиники, исключая занятые записи
- **Полнотекстовый поиск**: фильтр `?search=` по имени и описанию (LIKE + ILIKE)
- **Idempotent seed**: скрипт безопасно запускать повторно

---

## AI Summary

### 1. Роль ИИ в создании бэкенда

Весь бэкенд спроектирован и реализован с помощью ИИ (Claude, модель `claude-sonnet-4-6`). ИИ выступал в роли архитектора и разработчика: определял структуру проекта, выбирал технологии, генерировал ORM-модели, Pydantic-схемы, CRUD-слой, роутеры FastAPI, JWT-аутентификацию, миграции Alembic, seed-скрипт и Docker-конфигурацию. Человек формулировал требования и принимал решения по бизнес-логике.

### 2. Правила (требования) к реализации

1. **Пагинация** — все списочные эндпоинты должны поддерживать `?page=1&limit=20`
2. **Фильтрация и поиск** — полнотекстовый поиск по названию клиники/врача через `?search=`
3. **CORS** — разрешить запросы с фронтенда (localhost:3000, production domain)
4. **OpenAPI** — автоматическая документация на `/docs`
5. **Seed данные** — скрипт `seed.py` с 10+ клиниками, 30+ врачами, 50+ услугами для Алматы
6. **Обработка ошибок** — единый формат ошибок `{"detail": "message", "code": "ERROR_CODE"}`
7. **Логирование** — структурированные логи через `logging`
8. **Health check** — `GET /health` для мониторинга

### 3. Список использованных MCP/агентов

| Агент | Назначение |
|-------|-----------|
| **backend-architect** | Проектирование архитектуры, выбор технологического стека, определение границ сервисов, проектирование схемы БД и API-контрактов |
