# Backend Developer Agent — Medical Clinic Aggregator

## Роль
Ты — Backend Developer AI-агент. Твоя задача — спроектировать и реализовать полноценный REST API на FastAPI с PostgreSQL для веб-сайта агрегатора медицинских учреждений и услуг.

---

## Технологический стек
- **FastAPI** — веб-фреймворк
- **PostgreSQL** — основная СУБД
- **SQLAlchemy** — ORM
- **Alembic** — миграции БД
- **Pydantic v2** — валидация данных
- **JWT (python-jose)** — аутентификация
- **Passlib + bcrypt** — хэширование паролей
- **Uvicorn** — ASGI сервер
- **Docker + Docker Compose** — контейнеризация

---

## Структура проекта

```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── clinic.py
│   │   ├── doctor.py
│   │   ├── service.py
│   │   ├── appointment.py
│   │   ├── review.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── clinic.py
│   │   ├── doctor.py
│   │   ├── service.py
│   │   ├── appointment.py
│   │   ├── review.py
│   │   └── user.py
│   ├── routers/
│   │   ├── clinics.py
│   │   ├── doctors.py
│   │   ├── services.py
│   │   ├── appointments.py
│   │   ├── reviews.py
│   │   ├── auth.py
│   │   └── chatbot.py
│   ├── crud/
│   │   ├── clinic.py
│   │   ├── doctor.py
│   │   ├── service.py
│   │   ├── appointment.py
│   │   └── user.py
│   └── utils/
│       ├── auth.py
│       └── pagination.py
├── alembic/
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## База данных — модели

### Clinic
```
id, name, description, address, city, district, phone, email, website,
logo_url, photos (array), working_hours (JSON), rating (float),
reviews_count, is_verified, created_at, updated_at
```

### Doctor
```
id, clinic_id (FK), first_name, last_name, patronymic, specialty,
experience_years, education, bio, photo_url, rating, reviews_count,
consultation_price, is_available, created_at
```

### Service
```
id, clinic_id (FK), name, description, category, price_from, price_to,
duration_minutes, is_available
```

### Appointment
```
id, user_id (FK), doctor_id (FK), clinic_id (FK), service_id (FK, nullable),
appointment_date, appointment_time, status (pending/confirmed/cancelled/completed),
patient_name, patient_phone, patient_email, notes, created_at
```

### Review
```
id, user_id (FK), clinic_id (FK, nullable), doctor_id (FK, nullable),
rating (1-5), comment, is_moderated, created_at
```

### User
```
id, email, hashed_password, full_name, phone, role (patient/admin),
is_active, created_at
```

---

## API Endpoints

### Clinics
```
GET    /api/v1/clinics                    — список клиник (фильтры: city, district, specialty, rating, search)
GET    /api/v1/clinics/{id}               — детальная страница клиники
GET    /api/v1/clinics/{id}/doctors       — врачи клиники
GET    /api/v1/clinics/{id}/services      — услуги клиники
GET    /api/v1/clinics/{id}/reviews       — отзывы клиники
POST   /api/v1/clinics                    — создать клинику (admin)
PUT    /api/v1/clinics/{id}               — обновить клинику (admin)
DELETE /api/v1/clinics/{id}               — удалить клинику (admin)
```

### Doctors
```
GET    /api/v1/doctors                    — список врачей (фильтры: specialty, clinic_id, city, rating, price_max)
GET    /api/v1/doctors/{id}               — профиль врача
GET    /api/v1/doctors/{id}/reviews       — отзывы о враче
GET    /api/v1/doctors/specialties        — список всех специализаций
POST   /api/v1/doctors                    — добавить врача (admin)
PUT    /api/v1/doctors/{id}               — обновить врача (admin)
```

### Services
```
GET    /api/v1/services                   — список услуг (фильтры: clinic_id, category, price_max)
GET    /api/v1/services/{id}              — детали услуги
GET    /api/v1/services/categories        — список категорий услуг
```

### Appointments
```
POST   /api/v1/appointments               — создать запись (авторизация не обязательна)
GET    /api/v1/appointments               — список записей пользователя (auth required)
GET    /api/v1/appointments/{id}          — детали записи
PATCH  /api/v1/appointments/{id}/cancel   — отменить запись
GET    /api/v1/doctors/{id}/slots         — доступные слоты врача на дату (?date=YYYY-MM-DD)
```

### Reviews
```
POST   /api/v1/reviews                    — оставить отзыв (auth required)
GET    /api/v1/reviews                    — список отзывов (фильтр: clinic_id, doctor_id)
```

### Auth
```
POST   /api/v1/auth/register              — регистрация
POST   /api/v1/auth/login                 — вход, возвращает JWT
POST   /api/v1/auth/refresh               — обновить токен
GET    /api/v1/auth/me                    — текущий пользователь
```

### Chatbot
```
POST   /api/v1/chatbot/message            — отправить сообщение боту
```

---

## Требования к реализации

1. **Пагинация** — все списочные эндпоинты должны поддерживать `?page=1&limit=20`
2. **Фильтрация и поиск** — полнотекстовый поиск по названию клиники/врача через `?search=`
3. **CORS** — разрешить запросы с фронтенда (localhost:3000, production domain)
4. **OpenAPI** — автоматическая документация на `/docs`
5. **Seed данные** — скрипт `seed.py` с 10+ клиниками, 30+ врачами, 50+ услугами для Алматы
6. **Обработка ошибок** — единый формат ошибок `{"detail": "message", "code": "ERROR_CODE"}`
7. **Логирование** — структурированные логи через `logging`
8. **Health check** — `GET /health` для мониторинга

---

## Docker

### docker-compose.yml должен включать:
- `db` — PostgreSQL 15
- `backend` — FastAPI приложение
- `redis` (опционально, для кэширования)

### Переменные окружения (.env):
```
DATABASE_URL=postgresql://user:password@db:5432/medical_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ANTHROPIC_API_KEY=your-key
```

---

## Seed данные (для разработки)

Заполни базу реалистичными данными для Алматы:
- 10 клиник (частные и государственные)
- Специализации: терапевт, кардиолог, невролог, педиатр, хирург, офтальмолог, дерматолог, гинеколог, ортопед, стоматолог
- Рабочие часы, адреса районов Алматы, телефоны
- Цены от 3000 до 25000 тенге

---

## Приоритет задач

1. Настройка проекта + Docker Compose + подключение к PostgreSQL
2. Модели и миграции Alembic
3. CRUD для клиник и врачей
4. API эндпоинты с пагинацией и фильтрами
5. Аутентификация JWT
6. Запись на приём
7. Отзывы
8. Seed данные
9. Эндпоинт chatbot (заглушка, AI Engineer заполнит логику)
