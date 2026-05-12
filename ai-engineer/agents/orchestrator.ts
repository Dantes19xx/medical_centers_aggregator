import Anthropic from "@anthropic-ai/sdk";
import { tools, toolsMap } from "../tools";
import { memoryStore } from "../memory/memory-store";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || "",
});

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
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

Текущий контекст пользователя:
${JSON.stringify(userContext, null, 2)}
`;

  const messages: Anthropic.Messages.MessageParam[] = [
    ...history.map((m) => ({
      role: m.role,
      content: m.content,
    })),
    { role: "user", content: message },
  ];

  const toolDefinitions = tools.map((t) => ({
    name: t.name,
    description: t.description,
    input_schema: {
      type: "object" as const,
      properties: t.parameters,
      required: Object.keys(t.parameters).filter((k) =>
        // Mark all as required for simplicity; in real app, use optional marker
        true
      ),
    },
  }));

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 4096,
    system: systemPrompt,
    messages,
    tools: toolDefinitions,
  });

  const toolCalls: unknown[] = [];

  for (const block of response.content) {
    if (block.type === "tool_use") {
      const tool = toolsMap.get(block.name);
      if (tool) {
        const result = await tool.execute(block.input);
        toolCalls.push({
          tool: block.name,
          input: block.input,
          output: result,
        });

        // Save to memory
        await memoryStore.addInteraction(userId, {
          tool: block.name,
          input: block.input,
          output: result,
          timestamp: new Date().toISOString(),
        });
      }
    }
  }

  // Update user context in memory
  await memoryStore.updateUserContext(userId, {
    lastMessage: message,
    lastResponse: response.content
      .filter((c) => c.type === "text")
      .map((c) => (c as Anthropic.TextBlock).text)
      .join(" "),
    lastToolCalls: toolCalls,
  });

  const textResponse = response.content
    .filter((c) => c.type === "text")
    .map((c) => (c as Anthropic.TextBlock).text)
    .join(" ") || "Готово. Чем ещё могу помочь?";

  return { response: textResponse, toolCalls };
}
