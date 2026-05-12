import { db } from "../db";
import { getOpenAIClient, OPENAI_MODEL } from "../openai-client";

export async function researchCenters(
  query: string,
  specialization?: string,
  location?: string
): Promise<{ centers: unknown[]; summary: string }> {
  const centers = await db.getMedicalCenters({
    specialization: specialization?.toLowerCase(),
    location: location?.toLowerCase(),
    minRating: 0,
  });

  const systemPrompt = `
Ты — research-agent медицинского агрегатора. Твоя задача — проанализировать список клиник
и составить краткое, полезное резюме для пользователя на основе его запроса.

Правила:
- Выделяй 2-3 лучших варианта с обоснованием.
- Указывай рейтинг, адрес и специализации.
- Не давай медицинских советов — только информацию о клиниках.
- Отвечай на русском.
`;

  const userPrompt = `
Запрос пользователя: "${query}"

Найденные клиники (${centers.length}):
${JSON.stringify(centers, null, 2)}

Составь краткое резюме с рекомендациями.
`;

  const openai = getOpenAIClient();
  const response = await openai.chat.completions.create({
    model: OPENAI_MODEL,
    max_tokens: 2048,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
  });

  const summary = response.choices[0]?.message.content || "";

  return { centers, summary };
}
