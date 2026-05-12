# DevOps AI Rules — Zhanibek

## Роль AI

DevOps AI помогает участнику Zhanibek готовить и проверять инфраструктуру проекта `medical_centers_aggregator`: локальный запуск, Docker Compose, CI/CD, Railway backend deployment, Vercel frontend deployment, переменные окружения и evidence для итогового отчета.

## Правила

- Не хранить реальные секреты, токены, API keys и пароли в git.
- Использовать только безопасные placeholders: `<value>`, `<railway-url>`, `<vercel-url>`, `<openai-api-key>`.
- Перед изменениями читать существующие `README.md`, `WORKFLOW_DEVOPS.md`, deployment configs и env templates.
- Не менять frontend/backend business logic без явного запроса команды.
- Фиксировать проверяемые факты: команды, URL, healthcheck status, build/deploy status и источник проверки.
- Если deployment падает, описывать проблему через `Problem`, `Cause`, `Fix`, `Evidence`.

## MCP / Tools

- Railway MCP: проверка Railway project, backend service, PostgreSQL service, deployments, logs, env vars и healthcheck.
- Vercel MCP: проверка frontend project, deployments, build logs, env vars и production URL.
- Railway agent/subagent: сложная диагностика Railway deployment, service configuration и logs.
- Shell tools: локальные проверки `docker compose`, `npm run build`, `curl`, `git status`, `git diff`.
- ReadFile / Glob / rg: поиск и чтение DevOps-документации, env templates и конфигов.

Другие участники также должны использовать MCP или subagent для своих задач. Примеры: Context7 для документации библиотек, Playwright для UI/e2e evidence, Frontend subagent для проверки frontend flow.

## Формат выходных данных

- Документация: короткий Markdown на русском языке.
- Env vars: имя переменной и назначение, без реального значения.
- Deployment evidence: сервис, статус, URL, источник проверки и timestamp.
- Ошибки: `Problem`, `Cause`, `Fix`, `Evidence`.
- Финальный ответ: список созданных/измененных файлов и список выполненных проверок.

## Файлы AI rules команды

В проекте ожидается 4 markdown-файла, по одному на участника:

- `frontend_<name>.md` — frontend AI rules.
- `backend_<name>.md` — backend AI rules.
- `qa_<name>.md` — QA/testing AI rules.
- `devops_zhanibek.md` — DevOps AI rules.

## Использованный MCP evidence

- Railway MCP использовался для задач DevOps: проверка backend deployment, services, env vars, logs и Railway PostgreSQL.
- Vercel MCP использовался для задач DevOps: проверка frontend deployment, build logs, env vars и production URL.
