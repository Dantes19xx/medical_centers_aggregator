# MedGuide DevOps Runbook

Эта папка содержит шаблоны DevOps-части проекта MedGuide для 90-минутного семинара. Файлы лежат отдельно, чтобы DevOps-роль могла подготовить инфраструктуру и затем скопировать нужные шаблоны в корень проекта без прямого редактирования `frontend` или `backend`.

## Что внутри

- `docker-compose.dev.yml` — локальный запуск PostgreSQL + FastAPI backend + Vite frontend.
- `backend.Dockerfile` — шаблон Dockerfile для FastAPI на Python 3.11 slim.
- `railway.json` — шаблон Railway deploy config для backend.
- `vercel.json` — шаблон Vercel config для Vite SPA.
- `github-actions/*.yml` — шаблоны CI/CD workflow для GitHub Actions.
- `env/*.env.example` — примеры переменных окружения без реальных секретов.
- `WORKFLOW_DEVOPS.md` — секция для отчета/`WORKFLOW.md` с evidence по Railway MCP и Vercel MCP.
- `ai-rules/devops_zhanibek.md` — правила для AI DevOps-роли.

## Как применять

1. Скопировать `devops/docker-compose.dev.yml` в корень проекта как `docker-compose.dev.yml`.
2. Скопировать `devops/backend.Dockerfile` в `backend/Dockerfile` после появления backend-кода.
3. Скопировать `devops/railway.json` в `backend/railway.json` или адаптировать путь Dockerfile в Railway.
4. Скопировать `devops/vercel.json` в `frontend/vercel.json`.
5. Скопировать `devops/github-actions/*.yml` в `.github/workflows/`.
6. Скопировать `devops/env/backend.env.example` и `devops/env/frontend.env.example` в соответствующие `.env.example`.
7. Добавить реальные секреты только в Railway, Vercel и GitHub Secrets, не в git.

## Локальный запуск

```bash
export OPENAI_API_KEY="<your-openai-api-key>"
docker compose -f docker-compose.dev.yml up --build
```

Frontend ожидается на `http://localhost:3000`, backend на `http://localhost:8000`, PostgreSQL на `localhost:5432`.

## Важные допущения

- В текущем frontend уже используется `VITE_API_BASE_URL=http://localhost:8000/api/v1`, поэтому шаблоны используют `/api/v1`.
- Healthcheck для Railway задан как `/health`, потому что backend реализует этот endpoint в `app.main`.
- Backend-код и Alembic подтверждены. Для Railway оставить `alembic upgrade head && ...`.
- Для семинара предпочтительный деплой: GitHub integration в Railway/Vercel. Token-based `deploy.yml` оставлен как опциональный шаблон.

## MCP evidence

DevOps-роль должна использовать Railway MCP и Vercel MCP для проверки проектов, env vars, деплоев и логов. Результаты зафиксировать в `WORKFLOW_DEVOPS.md`, а при финальной сборке перенести секцию в общий `WORKFLOW.md`.
