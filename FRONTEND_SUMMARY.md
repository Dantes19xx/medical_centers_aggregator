# Frontend Summary — MedFind (Medical Clinic Aggregator)

## Обзор

Фронтенд реализован как SPA (Single Page Application) на React 18 + TypeScript с использованием Vite в качестве сборщика. Приложение представляет собой агрегатор медицинских учреждений и услуг города Алматы.

---

## Технологический стек

| Технология | Версия | Назначение |
|------------|--------|-----------|
| React | 18 | UI-фреймворк |
| TypeScript | 5 | Статическая типизация |
| Vite | 8 | Сборщик и dev-сервер |
| Tailwind CSS | 4 | Стилизация |
| React Router | 6 | Клиентская маршрутизация |
| TanStack Query | 5 | Серверное состояние и кэширование |
| Zustand | 5 | Глобальное состояние (авторизация) |
| Axios | 1 | HTTP-клиент |
| React Hook Form + Zod | — | Формы и валидация |
| date-fns | — | Работа с датами |

---

## Структура проекта

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts           — Axios instance с JWT-interceptor и auto-logout
│   │   ├── clinics.ts          — API методы для клиник
│   │   ├── doctors.ts          — API методы для врачей и специализаций
│   │   ├── appointments.ts     — API методы для записей на приём
│   │   └── chatbot.ts          — API метод для чат-бота
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx      — Навигация, авторизация, логотип
│   │   │   ├── Footer.tsx      — Ссылки, контакты
│   │   │   └── Layout.tsx      — Обёртка с Outlet
│   │   ├── clinic/
│   │   │   └── ClinicCard.tsx  — Карточка клиники (лого, адрес, рейтинг, кнопки)
│   │   ├── doctor/
│   │   │   └── DoctorCard.tsx  — Карточка врача (фото, специальность, цена, кнопки)
│   │   ├── chatbot/
│   │   │   └── ChatbotWidget.tsx — Чат-бот виджет (floating, сессии, быстрые ответы)
│   │   └── ui/
│   │       └── StarRating.tsx  — Звёздный рейтинг с количеством отзывов
│   ├── pages/
│   │   ├── HomePage.tsx        — Главная: hero, специализации, как это работает
│   │   ├── ClinicsPage.tsx     — Список клиник с фильтрами и пагинацией
│   │   └── DoctorsPage.tsx     — Список врачей с фильтрами по специальности и цене
│   ├── store/
│   │   └── authStore.ts        — Zustand store: user, token, login/logout
│   ├── types/
│   │   └── index.ts            — TypeScript интерфейсы: Clinic, Doctor, Service, Appointment, User, ChatMessage
│   └── App.tsx                 — Роутер, QueryClient, ChatbotWidget
├── .env.example                — Шаблон переменных окружения
├── vite.config.ts              — Vite + Tailwind plugin, порт 3000
└── package.json
```

---

## Реализованные страницы

### Главная страница (`/`)
- Hero-секция с поисковой строкой
- Сетка из 12 специализаций врачей (иконки, клик → переход к врачам)
- Блок "Как это работает" (3 шага)

### Список клиник (`/clinics`)
- Фильтры: поиск по названию, район (6 районов Алматы), рейтинг
- Карточки клиник: лого, адрес, рейтинг, верификация, телефон
- Skeleton-загрузка, пустое состояние, пагинация
- Сброс фильтров

### Список врачей (`/doctors`)
- Фильтры: специализация (из API), цена до (слайдер 1 000–30 000 ₸)
- Карточки врачей: фото, ФИО, специальность, стаж, рейтинг, цена
- Пагинация с номером страницы

---

## Ключевые технические решения

### API Client (`src/api/client.ts`)
- Базовый URL из `VITE_API_BASE_URL`
- Request interceptor: автоматически добавляет `Authorization: Bearer <token>`
- Response interceptor: при 401 — очищает токен и редиректит на `/login`

### Авторизация (`src/store/authStore.ts`)
- JWT хранится в `localStorage`
- Zustand store с методами `setAuth` и `logout`
- Инициализация из localStorage при загрузке

### Чат-бот (`src/components/chatbot/ChatbotWidget.tsx`)
- Floating-кнопка в правом нижнем углу
- Session ID в `localStorage` (уникальный UUID)
- История сообщений (последние 10)
- Индикатор загрузки, быстрые подсказки (`suggestions`)
- `data-testid` атрибуты для Playwright E2E тестов

### TypeScript типы (`src/types/index.ts`)
Полный набор интерфейсов:
- `Clinic`, `Doctor`, `Service`, `Appointment`, `Review`, `User`
- `PaginatedResponse<T>` — универсальный тип для пагинированных ответов
- `ChatMessage`, `ChatResponse` — типы для чат-бота

---

## Запуск локально

```bash
cd frontend

# Установить зависимости
npm install

# Создать .env файл
cp .env.example .env
# Указать VITE_API_BASE_URL=http://localhost:8000/api/v1

# Запустить dev-сервер
npm run dev
# → http://localhost:3000

# Сборка для production
npm run build
```

---

## Переменные окружения

| Переменная | Описание | Пример |
|------------|---------|--------|
| `VITE_API_BASE_URL` | Базовый URL бэкенд API | `http://localhost:8000/api/v1` |
| `VITE_APP_NAME` | Название приложения | `MedFind` |

---

## Что предстоит реализовать

- [ ] Страница детального просмотра клиники (`/clinics/:id`) с табами
- [ ] Страница профиля врача (`/doctors/:id`)
- [ ] Страница услуг (`/services`)
- [ ] Форма записи на приём (wizard: 4 шага)
- [ ] Страницы авторизации (`/login`, `/register`)
- [ ] Личный кабинет пользователя (`/profile`)
- [ ] Интеграция с реальным API бэкенда
- [ ] E2E тесты на Playwright
- [ ] Деплой на Vercel

---

## Дизайн-система

- **Основной цвет:** `#2563EB` (blue-600)
- **CTA цвет:** `#16A34A` (green-600)
- **Шрифт:** Inter (system-ui fallback)
- **Подход:** Mobile-first, Tailwind utility classes
- **Карточки:** белый фон, `border-gray-200`, `hover:shadow-md`
- **Skeleton:** `animate-pulse` для состояний загрузки

---

*Дата последнего обновления: 12 мая 2026*
