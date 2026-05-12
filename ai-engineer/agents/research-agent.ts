import Anthropic from "@anthropic-ai/sdk";
import { db } from "../db";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || "",
});

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

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 2048,
    system: systemPrompt,
    messages: [{ role: "user", content: userPrompt }],
  });

  const summary = response.content
    .filter((c) => c.type === "text")
    .map((c) => (c as Anthropic.TextBlock).text)
    .join(" ");

  return { centers, summary };
}
