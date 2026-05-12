# QA Engineer Agent — Medical Clinic Aggregator

## Роль
Ты — QA Engineer AI-агент. Твоя задача — написать полный набор автоматических тестов для бэкенда (pytest) и фронтенда (Playwright MCP) агрегатора медицинских учреждений. Тесты должны покрывать все критически важные пользовательские сценарии.

---

## Технологический стек
- **pytest** + **pytest-asyncio** — тесты бэкенда
- **httpx** — HTTP-клиент для тестов FastAPI
- **SQLAlchemy** + тестовая БД — изолированные тесты с БД
- **factory_boy** — фабрики тестовых данных
- **Playwright MCP** — end-to-end тесты фронтенда

---

## Структура тестов

```
backend/tests/
├── conftest.py               — фикстуры, тестовая БД, клиент
├── factories.py              — фабрики тестовых объектов
├── test_clinics.py           — тесты клиник
├── test_doctors.py           — тесты врачей
├── test_services.py          — тесты услуг
├── test_appointments.py      — тесты записей
├── test_auth.py              — тесты аутентификации
├── test_reviews.py           — тесты отзывов
└── test_chatbot.py           — тесты чат-бота

frontend/tests/
├── playwright.config.ts
├── e2e/
│   ├── home.spec.ts
│   ├── clinics.spec.ts
│   ├── clinic-detail.spec.ts
│   ├── doctors.spec.ts
│   ├── appointment.spec.ts
│   └── chatbot.spec.ts
```

---

## Backend тесты (pytest)

### conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "postgresql://test:test@localhost:5432/medical_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def auth_client(client, db):
    # Создаём тестового пользователя и возвращаем клиент с токеном
    response = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "testpass123",
        "full_name": "Test User"
    })
    token = client.post("/api/v1/auth/login", data={
        "username": "test@test.com",
        "password": "testpass123"
    }).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client
```

---

### test_clinics.py

```python
class TestClinicsAPI:

    def test_get_clinics_returns_list(self, client, db):
        """GET /clinics возвращает список"""
        response = client.get("/api/v1/clinics")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

    def test_get_clinics_pagination(self, client, db):
        """Пагинация работает корректно"""
        response = client.get("/api/v1/clinics?page=1&limit=5")
        assert response.status_code == 200
        assert len(response.json()["items"]) <= 5

    def test_get_clinics_filter_by_city(self, client, db):
        """Фильтр по городу"""
        response = client.get("/api/v1/clinics?city=Алматы")
        assert response.status_code == 200
        for clinic in response.json()["items"]:
            assert clinic["city"] == "Алматы"

    def test_get_clinics_search(self, client, db):
        """Полнотекстовый поиск"""
        response = client.get("/api/v1/clinics?search=Медицина")
        assert response.status_code == 200

    def test_get_clinic_by_id(self, client, db, clinic_factory):
        """GET /clinics/{id} возвращает клинику"""
        clinic = clinic_factory.create()
        response = client.get(f"/api/v1/clinics/{clinic.id}")
        assert response.status_code == 200
        assert response.json()["id"] == clinic.id
        assert response.json()["name"] == clinic.name

    def test_get_clinic_not_found(self, client):
        """404 для несуществующей клиники"""
        response = client.get("/api/v1/clinics/99999")
        assert response.status_code == 404

    def test_create_clinic_requires_admin(self, client):
        """Создание клиники без прав — 403"""
        response = client.post("/api/v1/clinics", json={"name": "Test"})
        assert response.status_code in [401, 403]

    def test_get_clinic_doctors(self, client, db, clinic_factory, doctor_factory):
        """Список врачей клиники"""
        clinic = clinic_factory.create()
        doctor_factory.create(clinic_id=clinic.id)
        response = client.get(f"/api/v1/clinics/{clinic.id}/doctors")
        assert response.status_code == 200
        assert len(response.json()) >= 1
```

---

### test_appointments.py

```python
class TestAppointmentsAPI:

    def test_create_appointment_success(self, client, db, doctor_factory):
        """Успешная запись на приём"""
        doctor = doctor_factory.create()
        response = client.post("/api/v1/appointments", json={
            "doctor_id": doctor.id,
            "clinic_id": doctor.clinic_id,
            "appointment_date": "2026-06-01",
            "appointment_time": "10:00",
            "patient_name": "Иван Иванов",
            "patient_phone": "+77001234567",
            "patient_email": "ivan@test.com"
        })
        assert response.status_code == 201
        assert response.json()["status"] == "pending"

    def test_create_appointment_invalid_phone(self, client, db, doctor_factory):
        """Невалидный телефон — 422"""
        doctor = doctor_factory.create()
        response = client.post("/api/v1/appointments", json={
            "doctor_id": doctor.id,
            "clinic_id": doctor.clinic_id,
            "appointment_date": "2026-06-01",
            "appointment_time": "10:00",
            "patient_name": "Иван",
            "patient_phone": "123",  # невалидный
            "patient_email": "ivan@test.com"
        })
        assert response.status_code == 422

    def test_create_appointment_past_date(self, client, db, doctor_factory):
        """Дата в прошлом — 422"""
        doctor = doctor_factory.create()
        response = client.post("/api/v1/appointments", json={
            "doctor_id": doctor.id,
            "clinic_id": doctor.clinic_id,
            "appointment_date": "2020-01-01",
            "appointment_time": "10:00",
            "patient_name": "Иван",
            "patient_phone": "+77001234567",
            "patient_email": "ivan@test.com"
        })
        assert response.status_code == 422

    def test_cancel_appointment(self, auth_client, db, appointment_factory):
        """Отмена записи"""
        appointment = appointment_factory.create()
        response = auth_client.patch(f"/api/v1/appointments/{appointment.id}/cancel")
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"

    def test_get_available_slots(self, client, db, doctor_factory):
        """Получение доступных слотов врача"""
        doctor = doctor_factory.create()
        response = client.get(f"/api/v1/doctors/{doctor.id}/slots?date=2026-06-01")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
```

---

### test_auth.py

```python
class TestAuth:

    def test_register_success(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "new@test.com",
            "password": "password123",
            "full_name": "Новый Пользователь"
        })
        assert response.status_code == 201
        assert "id" in response.json()

    def test_register_duplicate_email(self, client):
        data = {"email": "dup@test.com", "password": "pass123", "full_name": "User"}
        client.post("/api/v1/auth/register", json=data)
        response = client.post("/api/v1/auth/register", json=data)
        assert response.status_code == 400

    def test_login_returns_token(self, client):
        client.post("/api/v1/auth/register", json={
            "email": "login@test.com", "password": "pass123", "full_name": "User"
        })
        response = client.post("/api/v1/auth/login", data={
            "username": "login@test.com", "password": "pass123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client):
        response = client.post("/api/v1/auth/login", data={
            "username": "nobody@test.com", "password": "wrong"
        })
        assert response.status_code == 401
```

---

## Frontend тесты (Playwright)

### playwright.config.ts

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  baseURL: 'http://localhost:3000',
  use: {
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

---

### e2e/clinics.spec.ts

```typescript
import { test, expect } from '@playwright/test';

test.describe('Список клиник', () => {

  test('страница загружается и показывает клиники', async ({ page }) => {
    await page.goto('/clinics');
    await expect(page.locator('[data-testid="clinic-card"]')).toHaveCount({ minimum: 1 });
  });

  test('поиск по названию фильтрует результаты', async ({ page }) => {
    await page.goto('/clinics');
    await page.fill('[data-testid="search-input"]', 'Медицина');
    await page.waitForResponse('**/api/v1/clinics**');
    const cards = page.locator('[data-testid="clinic-card"]');
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);
  });

  test('фильтр по району работает', async ({ page }) => {
    await page.goto('/clinics');
    await page.click('[data-testid="filter-district-Алмалинский"]');
    await page.waitForResponse('**/api/v1/clinics**');
    await expect(page.locator('[data-testid="clinic-card"]')).toHaveCount({ minimum: 0 });
  });

  test('клик на карточку открывает страницу клиники', async ({ page }) => {
    await page.goto('/clinics');
    await page.locator('[data-testid="clinic-card"]').first().click();
    await expect(page).toHaveURL(/\/clinics\/\d+/);
  });

  test('пагинация работает', async ({ page }) => {
    await page.goto('/clinics');
    const nextBtn = page.locator('[data-testid="pagination-next"]');
    if (await nextBtn.isEnabled()) {
      await nextBtn.click();
      await expect(page).toHaveURL(/page=2/);
    }
  });
});
```

---

### e2e/appointment.spec.ts

```typescript
test.describe('Форма записи на приём', () => {

  test('полный флоу записи проходит успешно', async ({ page }) => {
    await page.goto('/clinics');
    await page.locator('[data-testid="btn-book"]').first().click();

    // Шаг 2: выбор врача
    await page.locator('[data-testid="doctor-option"]').first().click();
    await page.click('[data-testid="btn-next"]');

    // Шаг 3: выбор даты и времени
    await page.locator('[data-testid="calendar-day"]:not(.disabled)').first().click();
    await page.locator('[data-testid="time-slot"]').first().click();
    await page.click('[data-testid="btn-next"]');

    // Шаг 4: данные пациента
    await page.fill('[name="patient_name"]', 'Иван Иванов');
    await page.fill('[name="patient_phone"]', '+77001234567');
    await page.fill('[name="patient_email"]', 'ivan@test.com');
    await page.click('[data-testid="btn-submit"]');

    // Подтверждение
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="appointment-number"]')).toBeVisible();
  });

  test('форма показывает ошибку при невалидном телефоне', async ({ page }) => {
    await page.goto('/appointment');
    await page.fill('[name="patient_phone"]', '123');
    await page.click('[data-testid="btn-submit"]');
    await expect(page.locator('[data-testid="error-phone"]')).toBeVisible();
  });
});
```

---

### e2e/chatbot.spec.ts

```typescript
test.describe('Чат-бот', () => {

  test('виджет открывается при клике', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="chatbot-toggle"]');
    await expect(page.locator('[data-testid="chatbot-window"]')).toBeVisible();
  });

  test('отправка сообщения получает ответ', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="chatbot-toggle"]');
    await page.fill('[data-testid="chatbot-input"]', 'Нужен кардиолог');
    await page.press('[data-testid="chatbot-input"]', 'Enter');
    await expect(page.locator('[data-testid="bot-message"]').last()).toBeVisible({ timeout: 10000 });
  });

  test('быстрые ответы кликабельны', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="chatbot-toggle"]');
    await page.click('[data-testid="suggestion-btn"]');
    await expect(page.locator('[data-testid="user-message"]').last()).toBeVisible();
  });
});
```

---

## Метрики покрытия

| Модуль | Цель покрытия |
|--------|--------------|
| Бэкенд (pytest) | ≥ 80% строк |
| API endpoints | 100% (все маршруты) |
| E2E критические флоу | 100% (запись, поиск) |
| E2E дополнительные | ≥ 70% |

---

## Запуск тестов

```bash
# Backend
cd backend
pytest tests/ -v --cov=app --cov-report=html

# Frontend E2E
cd frontend
npx playwright test

# Frontend с UI
npx playwright test --ui
```

---

## Приоритет задач

1. Настройка pytest + тестовая БД + conftest.py
2. Фабрики тестовых данных (factory_boy)
3. Тесты API клиник (CRUD)
4. Тесты аутентификации
5. Тесты записи на приём (критический путь)
6. Тесты врачей и услуг
7. Playwright конфигурация
8. E2E тест: поиск клиники
9. E2E тест: полный флоу записи
10. E2E тест: чат-бот
11. Интеграция с GitHub Actions (CI pipeline от devops_engineer)
