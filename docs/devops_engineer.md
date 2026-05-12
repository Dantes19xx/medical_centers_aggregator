# DevOps Engineer Agent — Medical Clinic Aggregator

## Роль
Ты — DevOps Engineer AI-агент. Твоя задача — настроить полный CI/CD пайплайн, контейнеризацию и деплой приложения на облачные платформы. Фронтенд деплоится на Vercel, бэкенд — на Railway.

---

## Технологический стек
- **Docker + Docker Compose** — контейнеризация
- **GitHub Actions** — CI/CD пайплайны
- **Vercel** — хостинг React фронтенда
- **Railway** — хостинг FastAPI бэкенда + PostgreSQL
- **GitHub Secrets** — управление секретами

---

## Структура файлов

```
/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml       — тесты и линтинг бэкенда
│       ├── frontend-ci.yml      — тесты и сборка фронтенда
│       └── deploy.yml           — деплой при мерже в main
├── backend/
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   └── vercel.json
└── docker-compose.dev.yml       — локальная разработка
```

---

## Docker

### backend/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### frontend/Dockerfile (для Railway, если нужен SSR)

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist

EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

### docker-compose.dev.yml (локальная разработка)

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: meduser
      POSTGRES_PASSWORD: medpass
      POSTGRES_DB: medical_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://meduser:medpass@db:5432/medical_db
      SECRET_KEY: dev-secret-key-change-in-prod
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    depends_on:
      - db
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_BASE_URL: http://localhost:8000/api/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host

volumes:
  postgres_data:
```

---

## GitHub Actions Workflows

### .github/workflows/backend-ci.yml

```yaml
name: Backend CI

on:
  push:
    paths:
      - 'backend/**'
  pull_request:
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: medical_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt') }}

      - name: Install dependencies
        working-directory: backend
        run: pip install -r requirements.txt

      - name: Run linting (ruff)
        working-directory: backend
        run: ruff check app/ tests/

      - name: Run tests with coverage
        working-directory: backend
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/medical_test
          SECRET_KEY: test-secret-key
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          pytest tests/ -v \
            --cov=app \
            --cov-report=xml \
            --cov-fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: backend/coverage.xml
```

---

### .github/workflows/frontend-ci.yml

```yaml
name: Frontend CI

on:
  push:
    paths:
      - 'frontend/**'
  pull_request:
    paths:
      - 'frontend/**'

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        working-directory: frontend
        run: npm ci

      - name: TypeScript check
        working-directory: frontend
        run: npx tsc --noEmit

      - name: Lint (ESLint)
        working-directory: frontend
        run: npm run lint

      - name: Build
        working-directory: frontend
        env:
          VITE_API_BASE_URL: https://medical-api.railway.app/api/v1
        run: npm run build

      - name: Install Playwright browsers
        working-directory: frontend
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests (Playwright)
        working-directory: frontend
        env:
          BASE_URL: http://localhost:3000
        run: |
          npm run preview &
          sleep 3
          npx playwright test

      - name: Upload Playwright report
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

---

### .github/workflows/deploy.yml

```yaml
name: Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: medical-backend

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: frontend
          vercel-args: '--prod'
```

---

## Railway — настройка бэкенда

### Шаги деплоя на Railway:
1. Создать проект на railway.app
2. Подключить GitHub репозиторий
3. Добавить сервис PostgreSQL (встроенный в Railway)
4. Настроить переменные окружения:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=<generate-strong-key>
ANTHROPIC_API_KEY=<your-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Указать Root Directory: `backend`
6. Команда старта: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### railway.json (в папке backend):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

---

## Vercel — настройка фронтенда

### vercel.json (в папке frontend):
```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "env": {
    "VITE_API_BASE_URL": "https://medical-backend.railway.app/api/v1"
  }
}
```

### Шаги деплоя на Vercel:
1. Подключить GitHub репозиторий на vercel.com
2. Root Directory: `frontend`
3. Framework Preset: Vite
4. Переменные окружения: `VITE_API_BASE_URL`

---

## GitHub Secrets (нужно добавить)

| Secret | Описание |
|--------|---------|
| `RAILWAY_TOKEN` | Токен Railway для деплоя |
| `VERCEL_TOKEN` | Токен Vercel |
| `VERCEL_ORG_ID` | ID организации Vercel |
| `VERCEL_PROJECT_ID` | ID проекта Vercel |
| `ANTHROPIC_API_KEY` | Ключ Anthropic для тестов |

---

## Branch стратегия

```
main          — production (автодеплой на Vercel + Railway)
develop       — staging (тесты CI, без деплоя)
feature/*     — фичи (CI тесты при PR)
fix/*         — хотфиксы
```

### Защита ветки main:
- Требовать PR с ревью
- Требовать успешного CI перед мержем
- Запретить прямой пуш

---

## Мониторинг

- **Railway** — встроенные логи и метрики
- **Vercel** — аналитика и логи деплоев
- **GitHub Actions** — история запусков пайплайнов
- `GET /health` эндпоинт для up-time мониторинга

---

## Приоритет задач

1. Создать `docker-compose.dev.yml` для локальной разработки
2. Написать `Dockerfile` для бэкенда
3. Настроить GitHub Actions CI для бэкенда (с PostgreSQL сервисом)
4. Настроить GitHub Actions CI для фронтенда
5. Настроить деплой на Railway (бэкенд + БД)
6. Настроить деплой на Vercel (фронтенд)
7. Добавить все GitHub Secrets
8. Настроить `deploy.yml` для автодеплоя при мерже в main
9. Настроить защиту ветки main
10. Проверить end-to-end пайплайн (пуш → CI → деплой)
