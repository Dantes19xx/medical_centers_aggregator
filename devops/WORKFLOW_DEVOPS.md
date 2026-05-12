# DevOps Workflow Section

## Role

DevOps Engineer prepares CI/CD, local development, environment templates, and deployment evidence for MedGuide.

## Files Created

- `devops/README.md` — DevOps runbook.
- `devops/docker-compose.dev.yml` — local PostgreSQL + backend + frontend.
- `devops/backend.Dockerfile` — FastAPI Dockerfile template for Railway.
- `devops/railway.json` — Railway backend deploy config.
- `devops/vercel.json` — Vite SPA config for Vercel.
- `devops/github-actions/backend-ci.yml` — backend CI with PostgreSQL service.
- `devops/github-actions/frontend-ci.yml` — frontend CI.
- `devops/github-actions/deploy.yml` — optional token-based deploy workflow.
- `devops/env/backend.env.example` — backend env template.
- `devops/env/frontend.env.example` — frontend env template.
- `devops/ai-rules/devops_zhanibek.md` — AI rules for DevOps role.

## Railway MCP Evidence Checklist

- [ ] Railway MCP connected in Cursor.
- [ ] Railway OAuth authorization completed.
- [ ] Railway project found or created: `<project-name>`.
- [ ] Backend service checked: `<backend-service-name>`.
- [ ] PostgreSQL service checked: `<postgres-service-name>`.
- [ ] Env vars checked: `DATABASE_URL`, `OPENAI_API_KEY`, `SECRET_KEY`, `CORS_ORIGINS`, `ENVIRONMENT`.
- [ ] Deployment status checked: `<status>`.
- [ ] Backend logs checked for startup errors.
- [ ] Healthcheck checked: `/api/health`.

## Vercel MCP Evidence Checklist

- [ ] Vercel MCP connected in Cursor.
- [ ] Vercel OAuth authorization completed.
- [ ] Vercel project found or created: `<project-name>`.
- [ ] Framework preset checked: Vite.
- [ ] Build settings checked: `npm run build`, output `dist`.
- [ ] Env var checked: `VITE_API_BASE_URL`.
- [ ] Production deployment checked: `<status>`.
- [ ] Build logs checked for errors.

## Deployment URLs

- Frontend: `<https://your-vercel-app.vercel.app>`
- Backend: `<https://your-railway-service.up.railway.app>`
- Healthcheck: `<https://your-railway-service.up.railway.app/api/health>`

## Problems And Fixes

- Problem: `<what failed>`
- Cause: `<why it failed>`
- Fix: `<what was changed>`
- Evidence: `<MCP check, log line, screenshot, or URL>`

## Screenshots

- [ ] Railway services screenshot: `<path-or-link>`
- [ ] Railway env vars screenshot with secrets hidden: `<path-or-link>`
- [ ] Vercel deployment screenshot: `<path-or-link>`
- [ ] GitHub Actions CI screenshot: `<path-or-link>`

## Notes

- Use `OPENAI_API_KEY`, not Anthropic keys.
- Do not commit real secrets or tokens.
- Preferred seminar deploy path: GitHub integration in Railway and Vercel.
- Optional path: token-based `devops/github-actions/deploy.yml` after adding GitHub Secrets.
