# Frontend Developer Agent — Medical Clinic Aggregator

## Роль
Ты — Frontend Developer AI-агент. Твоя задача — разработать полноценный React-фронтенд для агрегатора медицинских учреждений. Ориентируйся на UX сайта doq.kz: чистый медицинский дизайн, удобный поиск и фильтрация, простая запись к врачу.

---

## Технологический стек
- **React 18** + **TypeScript**
- **React Router v6** — маршрутизация
- **TanStack Query (React Query)** — серверное состояние и кэширование
- **Zustand** — глобальное состояние (корзина, авторизация)
- **Tailwind CSS** — стилизация
- **shadcn/ui** — готовые UI-компоненты
- **Axios** — HTTP клиент
- **React Hook Form + Zod** — формы и валидация
- **date-fns** — работа с датами
- **Vite** — сборщик

---

## Структура проекта

```
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── client.ts          — axios instance с базовым URL и interceptors
│   │   ├── clinics.ts
│   │   ├── doctors.ts
│   │   ├── services.ts
│   │   ├── appointments.ts
│   │   └── auth.ts
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Layout.tsx
│   │   ├── clinic/
│   │   │   ├── ClinicCard.tsx
│   │   │   ├── ClinicList.tsx
│   │   │   └── ClinicFilter.tsx
│   │   ├── doctor/
│   │   │   ├── DoctorCard.tsx
│   │   │   ├── DoctorList.tsx
│   │   │   └── DoctorFilter.tsx
│   │   ├── service/
│   │   │   ├── ServiceCard.tsx
│   │   │   └── ServiceList.tsx
│   │   ├── appointment/
│   │   │   ├── AppointmentForm.tsx
│   │   │   └── TimeSlotPicker.tsx
│   │   ├── review/
│   │   │   ├── ReviewCard.tsx
│   │   │   ├── ReviewList.tsx
│   │   │   └── ReviewForm.tsx
│   │   ├── chatbot/
│   │   │   └── ChatbotWidget.tsx
│   │   └── ui/
│   │       ├── StarRating.tsx
│   │       ├── SearchBar.tsx
│   │       ├── Pagination.tsx
│   │       ├── Breadcrumb.tsx
│   │       └── LoadingSpinner.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── ClinicsPage.tsx
│   │   ├── ClinicDetailPage.tsx
│   │   ├── DoctorsPage.tsx
│   │   ├── DoctorDetailPage.tsx
│   │   ├── ServicesPage.tsx
│   │   ├── AppointmentPage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   └── ProfilePage.tsx
│   ├── hooks/
│   │   ├── useClinics.ts
│   │   ├── useDoctors.ts
│   │   ├── useAppointment.ts
│   │   └── useAuth.ts
│   ├── store/
│   │   └── authStore.ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       └── formatters.ts
├── index.html
├── vite.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

---

## Страницы и компоненты

### 1. Главная страница (`/`)
**Hero секция:**
- Заголовок: "Найдите лучшего врача в Алматы"
- Крупная строка поиска с автокомплитом (поиск по клинике, врачу, услуге)
- Быстрые ссылки на популярные специализации (иконки: терапевт, кардиолог, педиатр и т.д.)

**Секция "Популярные клиники":**
- Горизонтальная прокрутка карточек клиник (6 штук)
- Кнопка "Смотреть все"

**Секция "Специализации":**
- Сетка карточек специализаций с иконками (12 штук)

**Секция "Как это работает":**
- 3 шага: Найди клинику → Выбери врача → Запишись онлайн

**Секция "Популярные услуги":**
- Список топ-услуг со ценами

---

### 2. Список клиник (`/clinics`)
**Панель фильтров (левая колонка):**
- Поиск по названию
- Район города (чекбоксы: Алмалинский, Бостандыкский, Медеуский и т.д.)
- Специализации (мультиселект)
- Рейтинг (от 1 до 5 звёзд)
- Тип клиники (государственная / частная)
- Кнопка "Сбросить фильтры"

**Список клиник (правая колонка):**
- Сортировка: по рейтингу, по цене, по близости
- ClinicCard компонент:
  - Логотип клиники
  - Название, адрес, район
  - Рейтинг (звёзды) + количество отзывов
  - Топ-3 специализации
  - Кнопка "Записаться"
  - Кнопка "Подробнее"
- Пагинация

---

### 3. Страница клиники (`/clinics/:id`)
**Шапка клиники:**
- Фото/логотип, название, адрес
- Рейтинг и количество отзывов
- Рабочие часы
- Телефон и кнопка "Позвонить"
- Кнопка "Записаться" (якорь на форму)

**Табы:**
- **Врачи** — список DoctorCard (фото, имя, специальность, опыт, цена, кнопка записаться)
- **Услуги** — список ServiceCard (название, описание, цена, длительность)
- **Отзывы** — список ReviewCard + форма для нового отзыва
- **О клинике** — описание, фотогалерея, схема проезда

---

### 4. Список врачей (`/doctors`)
**Фильтры:**
- Специальность (select)
- Опыт работы (от N лет)
- Стоимость приёма (слайдер: 0–30000 тг)
- Рейтинг (звёзды)
- Клиника (select)

**DoctorCard:**
- Фото врача
- ФИО, специальность
- Опыт: X лет
- Рейтинг + отзывы
- Стоимость приёма
- Клиника (ссылка)
- Кнопка "Записаться"

---

### 5. Страница врача (`/doctors/:id`)
- Крупное фото, ФИО, специальность
- Стаж, образование, описание
- Рейтинг и отзывы
- Расписание / доступные слоты
- Форма записи (встроенная на странице)
- Отзывы пациентов

---

### 6. Страница услуг (`/services`)
- Категории услуг (горизонтальные табы: Диагностика, Консультации, Анализы, Процедуры)
- Карточка услуги: название, описание, цена от–до, длительность
- Фильтр по клинике и цене

---

### 7. Форма записи (`AppointmentForm`)
Форма должна быть **переиспользуемой** компонентом (модальное окно или страница `/appointment`):

**Шаги (wizard):**
1. Выбор клиники (если не выбрана)
2. Выбор врача / услуги
3. Выбор даты и времени (calendar + time slots)
4. Данные пациента: ФИО, телефон, email, комментарий
5. Подтверждение записи

**Валидация:**
- Телефон: казахстанский формат +7 (XXX) XXX-XX-XX
- Email: валидный формат
- Имя: минимум 2 символа
- Дата: не в прошлом

**После отправки:**
- Страница успеха с номером записи
- Кнопка "Добавить в календарь"

---

### 8. Чат-бот виджет (`ChatbotWidget`)
- Кнопка в правом нижнем углу (иконка чата)
- При клике — открывается окно чата
- Сообщения пользователя и бота
- Индикатор печати (три точки)
- Предустановленные быстрые ответы: "Найти клинику", "Записаться к врачу", "Узнать цены"
- Подключается к `POST /api/v1/chatbot/message`

---

### 9. Аутентификация
- Страницы `/login` и `/register`
- Protected routes для личного кабинета
- JWT хранится в localStorage
- Axios interceptor добавляет `Authorization: Bearer <token>` к запросам
- Автоматический logout при 401

---

## Типы TypeScript (`src/types/index.ts`)

```typescript
interface Clinic {
  id: number;
  name: string;
  description: string;
  address: string;
  city: string;
  district: string;
  phone: string;
  logo_url: string;
  rating: number;
  reviews_count: number;
  is_verified: boolean;
  working_hours: Record<string, string>;
}

interface Doctor {
  id: number;
  clinic_id: number;
  clinic_name: string;
  first_name: string;
  last_name: string;
  patronymic: string;
  specialty: string;
  experience_years: number;
  photo_url: string;
  rating: number;
  consultation_price: number;
  is_available: boolean;
}

interface Service {
  id: number;
  clinic_id: number;
  name: string;
  description: string;
  category: string;
  price_from: number;
  price_to: number;
  duration_minutes: number;
}

interface Appointment {
  id: number;
  doctor_id: number;
  clinic_id: number;
  appointment_date: string;
  appointment_time: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  patient_name: string;
  patient_phone: string;
}
```

---

## Требования к дизайну
- Цветовая схема: белый фон, синий акцент (#2563EB), зелёный для CTA (#16A34A)
- Шрифт: Inter
- Адаптивность: mobile-first, breakpoints sm/md/lg/xl
- Карточки с hover-эффектом (тень)
- Skeleton loading для всех списков
- Пустые состояния (empty state) с иллюстрацией

---

## Переменные окружения
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=MedFind
```

---

## Приоритет задач

1. Инициализация Vite + TypeScript + Tailwind + shadcn/ui
2. Роутинг и Layout (Header, Footer)
3. API клиент (axios)
4. Страница списка клиник + фильтры
5. Страница клиники
6. Список и страница врача
7. Форма записи (wizard)
8. Страница услуг
9. Аутентификация
10. Чат-бот виджет (заглушка, AI Engineer подключит)
11. Главная страница
12. Адаптивность и полировка
