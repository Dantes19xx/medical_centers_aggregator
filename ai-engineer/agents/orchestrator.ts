import type {
  ChatCompletionMessageParam,
  ChatCompletionTool,
} from "openai/resources/chat/completions";
import { tools, toolsMap } from "../tools";
import { memoryStore } from "../memory/memory-store";
import { getOpenAIClient, OPENAI_MODEL } from "../openai-client";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

function parseToolArguments(rawArguments: string): Record<string, unknown> {
  try {
    return JSON.parse(rawArguments || "{}");
  } catch {
    return {};
  }
}

export async function orchestrateChat(
  userId: string,
  message: string,
  history: ChatMessage[] = []
): Promise<{ response: string; toolCalls?: unknown[] }> {
  // Load user context from memory
  const userContext = await memoryStore.getUserContext(userId);

  const systemPrompt = `
Ты — AI-ассистент медицинского агрегатора. Ты помогаешь пользователям:
1. Найти подходящий медицинский центр
2. Записаться на приём
3. Получить предварительную информацию о симптомах (без постановки диагноза!)
4. Получить уведомления о записи

Правила:
- Ты ОБЯЗАН использовать инструменты (tools) для любых операций с данными.
- Не выдумывай данные — всегда вызывай соответствующий tool.
- Для медицинских вопросов давай только общую информацию и рекомендуй обратиться к врачу.
- Отвечай на русском языке, если пользователь пишет по-русски.
- Сохраняй контекст разговора для персонализации.
- Отвечай кратко, так как ответ показывается в маленьком чат-виджете.
- Для результатов поиска показывай максимум 3 варианта.
- Для каждого врача указывай только: имя, рейтинг, цену и клинику.
- Не добавляй длинные описания, образование, биографию, адрес, телефон или сайт, если пользователь прямо не попросил.
- Не используй большие markdown-разделы и заголовки. Лучше 2-4 короткие строки.
- В конце добавь короткий вопрос: "Хотите записаться?"

Текущий контекст пользователя:
${JSON.stringify(userContext, null, 2)}
`;

  const messages: ChatCompletionMessageParam[] = [
    { role: "system", content: systemPrompt },
    ...history.map((m) => ({
      role: m.role,
      content: m.content,
    })),
    { role: "user", content: message },
  ];

  const toolDefinitions: ChatCompletionTool[] = tools.map((t) => ({
    type: "function",
    function: {
      name: t.name,
      description: t.description,
      parameters: {
        type: "object",
        properties: t.parameters,
        required: t.required || Object.keys(t.parameters),
      },
    },
  }));

  const openai = getOpenAIClient();
  const response = await openai.chat.completions.create({
    model: OPENAI_MODEL,
    max_tokens: 4096,
    messages,
    tools: toolDefinitions,
    tool_choice: "auto",
  });

  const toolCalls: unknown[] = [];
  const assistantMessage = response.choices[0]?.message;
  const toolResultMessages: ChatCompletionMessageParam[] = [];

  for (const toolCall of assistantMessage?.tool_calls || []) {
    if (toolCall.type !== "function") continue;

    const tool = toolsMap.get(toolCall.function.name);
    if (tool) {
      const input = parseToolArguments(toolCall.function.arguments);
      const result = await tool.execute(input);
      toolCalls.push({
        tool: toolCall.function.name,
        input,
        output: result,
      });
      toolResultMessages.push({
        role: "tool",
        tool_call_id: toolCall.id,
        content: JSON.stringify(result),
      });

      // Save to memory
      await memoryStore.addInteraction(userId, {
        tool: toolCall.function.name,
        input,
        output: result,
        timestamp: new Date().toISOString(),
      });
    }
  }

  let textResponse = assistantMessage?.content || "";
  if (assistantMessage?.tool_calls?.length && toolResultMessages.length) {
    const finalResponse = await openai.chat.completions.create({
      model: OPENAI_MODEL,
      max_tokens: 2048,
      messages: [
        ...messages,
        {
          role: "assistant",
          content: assistantMessage.content || null,
          tool_calls: assistantMessage.tool_calls,
        },
        ...toolResultMessages,
      ],
    });

    textResponse = finalResponse.choices[0]?.message.content || textResponse;
  }

  if (!textResponse) {
    textResponse = "Готово. Чем ещё могу помочь?";
  }

  // Update user context in memory
  await memoryStore.updateUserContext(userId, {
    lastMessage: message,
    lastResponse: textResponse,
    lastToolCalls: toolCalls,
  });

  return { response: textResponse, toolCalls };
}
