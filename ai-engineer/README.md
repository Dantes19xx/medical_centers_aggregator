# AI Engineer — Мадина

Эта папка содержит всю работу AI Engineer (Lead Architect) для проекта Medical Centers Aggregator.

## Структура

```
ai-engineer/
├── ai_Madina.md              # Персональные AI-правила
├── README.md                 # Этот файл
├── package.json              # Зависимости backend
├── tsconfig.json             # TypeScript конфиг
├── jest.config.js            # Конфиг тестов
├── .env.example              # Пример переменных окружения
├── index.ts                  # Entry point Express сервера
├── db.ts                     # In-memory база данных (мок)
│
├── agents/                   # Sub-agents
│   ├── orchestrator.ts       # Главный оркестратор (Tools API)
│   ├── research-agent.ts     # Агент поиска клиник
│   ├── booking-agent.ts      # Агент записи на приём
│   └── symptom-agent.ts      # Агент анализа симптомов
│
├── tools/                    # Инструменты (Tools / MCP)
│   ├── index.ts              # Регистрация всех tools
│   ├── search-medical-centers.ts
│   ├── book-appointment.ts
│   ├── get-doctor-schedule.ts
│   ├── analyze-symptoms.ts
│   ├── send-notification.ts
│   ├── search-medical-centers.test.ts
│   └── analyze-symptoms.test.ts
│
├── api/                      # API routes
│   ├── ai-chat.ts            # AI chat, research, book, symptoms
│   ├── medical-centers.ts    # REST для клиник
│   └── appointments.ts       # REST для записей
│
└── memory/                   # Система памяти
    └── memory-store.ts       # In-memory контекст пользователя
```

## Архитектура

- **Orchestrator** — главный агент, общается с Claude API, выбирает и вызывает tools
- **Research Agent** — sub-agent для поиска и анализа клиник
- **Booking Agent** — sub-agent для процесса записи на приём
- **Symptom Checker Agent** — sub-agent для первичного сбора симптомов (без диагностики!)

## Tools

Все AI-вызовы используют **Tools API** (не raw chat):

- `search_medical_centers` — поиск по специализации, локации, рейтингу
- `book_appointment` — запись на приём
- `get_doctor_schedule` — получение расписания врача
- `analyze_symptoms` — предварительный анализ симптомов
- `send_notification` — уведомления пользователю

## Тесты

- `search-medical-centers.test.ts` — 4 тест-кейса
- `analyze-symptoms.test.ts` — 4 тест-кейса

Запуск: `npm test`

## MCP & Sub-agents

- Context7 MCP — документация
- Playwright MCP — браузерная автоматизация
- 3 sub-agents: research, booking, symptom-checker
