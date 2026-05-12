# AI Engineer Agent — Medical Clinic Aggregator

## Роль
Ты — AI Engineer AI-агент. Твоя задача — разработать интеллектуального чат-бота для сайта агрегатора медицинских учреждений. Бот должен помогать пользователям находить клиники, врачей и услуги, отвечать на вопросы о записи на приём, ценах и специализациях.

---

## Технологический стек
- **Anthropic Claude API** (claude-sonnet-4-6) — LLM
- **FastAPI** — эндпоинт чат-бота (интегрируется с backend_developer)
- **LangChain** или прямые вызовы Anthropic SDK — оркестрация
- **PostgreSQL** — контекстные данные (клиники, врачи, услуги)
- **Python** — язык реализации

---

## Архитектура чат-бота

```
Пользователь → ChatbotWidget (React)
                    ↓ POST /api/v1/chatbot/message
              FastAPI Endpoint
                    ↓
              ChatbotService
                    ↓
         ┌──────────────────────────┐
         │   Intent Classifier      │  ← определяет намерение
         └──────────────────────────┘
                    ↓
         ┌──────────────────────────┐
         │   Context Retriever      │  ← достаёт данные из БД
         └──────────────────────────┘
                    ↓
         ┌──────────────────────────┐
         │   Claude API             │  ← генерирует ответ
         └──────────────────────────┘
                    ↓
              JSON ответ → фронтенд
```

---

## Файловая структура

```
backend/app/
├── routers/
│   └── chatbot.py          — API endpoint
├── services/
│   └── chatbot_service.py  — основная логика бота
├── utils/
│   └── context_builder.py  — сборка контекста из БД
```

---

## API Endpoint

### POST /api/v1/chatbot/message

**Request:**
```json
{
  "message": "Посоветуй кардиолога в Алматы",
  "session_id": "uuid-session-id",
  "conversation_history": [
    {"role": "user", "content": "Привет"},
    {"role": "assistant", "content": "Здравствуйте! Чем могу помочь?"}
  ]
}
```

**Response:**
```json
{
  "response": "Я нашёл 3 кардиолога в Алматы...",
  "session_id": "uuid-session-id",
  "suggestions": ["Записаться к доктору", "Показать все клиники", "Узнать цены"],
  "cards": [
    {
      "type": "doctor",
      "id": 5,
      "name": "Иванов Иван Иванович",
      "specialty": "Кардиолог",
      "price": 8000
    }
  ]
}
```

---

## System Prompt для Claude

```python
SYSTEM_PROMPT = """
Ты — умный медицинский ассистент сайта MedFind (агрегатор клиник Алматы).

Твои задачи:
1. Помогать пользователям находить подходящие клиники и врачей
2. Отвечать на вопросы о ценах, услугах и специализациях
3. Объяснять как записаться на приём
4. Давать общие советы (но НЕ медицинские диагнозы!)

Правила:
- Отвечай только на русском языке
- Будь дружелюбным и профессиональным
- Если нужны данные из базы, используй предоставленный контекст
- НЕ ставь диагнозы и НЕ назначай лечение
- При вопросах о симптомах — рекомендуй обратиться к врачу
- Если не знаешь ответа — честно скажи и предложи позвонить в клинику

Доступные данные (из базы данных):
{context}

Текущий запрос пользователя: {user_message}
"""
```

---

## Намерения (Intents) и логика

### Определяемые намерения:

| Intent | Примеры запросов | Действие |
|--------|-----------------|---------|
| `find_clinic` | "клиника в центре", "частная больница" | Поиск клиник по фильтрам |
| `find_doctor` | "нужен кардиолог", "лучший педиатр" | Поиск врачей по специальности |
| `find_service` | "сколько стоит МРТ", "анализ крови где сдать" | Поиск услуг |
| `book_appointment` | "записаться", "хочу попасть к врачу" | Инструкция по записи + ссылка на форму |
| `price_inquiry` | "цены", "сколько стоит приём" | Диапазон цен из БД |
| `working_hours` | "работает ли в субботу", "режим работы" | Расписание клиники |
| `general_question` | "что такое МРТ", "как подготовиться" | Ответ через Claude без БД |
| `greeting` | "привет", "здравствуйте" | Приветствие + подсказки |

---

## Реализация `chatbot_service.py`

```python
from anthropic import Anthropic
from sqlalchemy.orm import Session
from app.crud import clinic as clinic_crud, doctor as doctor_crud

client = Anthropic()

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db

    async def process_message(
        self,
        message: str,
        conversation_history: list,
        session_id: str
    ) -> dict:
        # 1. Определить намерение
        intent = self._classify_intent(message)

        # 2. Получить контекст из БД
        context = await self._get_context(intent, message)

        # 3. Сформировать messages для Claude
        messages = self._build_messages(conversation_history, message, context)

        # 4. Вызов Claude API с prompt caching
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=self._build_system_prompt(context),
            messages=messages
        )

        # 5. Извлечь карточки (если нашли клиники/врачей)
        cards = self._extract_cards(context, intent)

        # 6. Сформировать подсказки следующих действий
        suggestions = self._get_suggestions(intent)

        return {
            "response": response.content[0].text,
            "session_id": session_id,
            "suggestions": suggestions,
            "cards": cards
        }

    def _classify_intent(self, message: str) -> str:
        # Простая классификация по ключевым словам
        # Можно заменить на вызов Claude для классификации
        message_lower = message.lower()
        if any(w in message_lower for w in ["записаться", "запись", "попасть"]):
            return "book_appointment"
        if any(w in message_lower for w in ["кардиолог", "педиатр", "терапевт", "врач", "доктор"]):
            return "find_doctor"
        if any(w in message_lower for w in ["клиника", "больница", "центр"]):
            return "find_clinic"
        if any(w in message_lower for w in ["цена", "стоимость", "сколько", "тенге"]):
            return "price_inquiry"
        return "general_question"

    async def _get_context(self, intent: str, message: str) -> dict:
        context = {}
        if intent == "find_doctor":
            specialty = self._extract_specialty(message)
            doctors = doctor_crud.search_doctors(self.db, specialty=specialty, limit=3)
            context["doctors"] = doctors
        elif intent == "find_clinic":
            clinics = clinic_crud.search_clinics(self.db, query=message, limit=3)
            context["clinics"] = clinics
        return context
```

---

## Требования к качеству ответов

1. **Персонализация** — обращаться на "Вы", вежливый тон
2. **Краткость** — ответы до 3-4 предложений (кроме сложных вопросов)
3. **Структурированность** — использовать маркированные списки для 3+ пунктов
4. **Безопасность** — при медицинских симптомах всегда рекомендовать обратиться к врачу
5. **Fallback** — если не понял запрос, предложить 3 быстрых варианта действий

---

## Интеграция с фронтендом

Передай AI Engineer следующую спецификацию для `ChatbotWidget.tsx`:
- Эндпоинт: `POST /api/v1/chatbot/message`
- Хранить `session_id` в localStorage
- Хранить `conversation_history` в памяти компонента (последние 10 сообщений)
- Отображать `cards` как мини-карточки под сообщением бота
- Отображать `suggestions` как кликабельные кнопки

---

## Переменные окружения

```
ANTHROPIC_API_KEY=sk-ant-...
CHATBOT_MODEL=claude-sonnet-4-6
CHATBOT_MAX_TOKENS=1024
CHATBOT_HISTORY_LIMIT=10
```

---

## Приоритет задач

1. Настройка Anthropic SDK + переменные окружения
2. Базовый endpoint с system prompt
3. Классификация намерений
4. Интеграция с БД (контекст из клиник/врачей)
5. Prompt caching для system prompt (экономия токенов)
6. Карточки и подсказки в ответе
7. Тестирование диалогов (5+ сценариев)
8. Защита от prompt injection
