import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || "",
});

export interface SymptomInput {
  symptoms: string;
  age?: number;
  gender?: string;
}

export async function analyzeSymptomsWithAgent(
  input: SymptomInput
): Promise<{
  analysis: string;
  recommendedSpecializations: string[];
  disclaimer: string;
}> {
  const systemPrompt = `
Ты — symptom-checker-agent медицинского агрегатора. Твоя задача — провести первичный сбор
симптомов и предложить направление к нужному специалисту.

⚠️ КРИТИЧЕСКИ ВАЖНО:
- Ты НЕ ставишь медицинский диагноз.
- Ты даёшь только предварительную рекомендацию по специализации.
- Всегда направляй к врачу для точной диагностики.
- Если симптомы указывают на экстренную ситуацию — рекомендуй вызвать скорую помощь (103).

Отвечай на русском языке.
`;

  const userPrompt = `
Пациент сообщает следующие симптомы: "${input.symptoms}"
Возраст: ${input.age || "не указан"}
Пол: ${input.gender || "не указан"}

Определи:
1. Возможные направления (специализации)
2. Уровень срочности
3. Общие рекомендации
`;

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 2048,
    system: systemPrompt,
    messages: [{ role: "user", content: userPrompt }],
  });

  const analysis = response.content
    .filter((c) => c.type === "text")
    .map((c) => (c as Anthropic.TextBlock).text)
    .join(" ");

  // Extract specializations heuristically
  const specKeywords: Record<string, string> = {
    кардиолог: "кардиология",
    невролог: "неврология",
    терапевт: "терапия",
    гастроэнтеролог: "гастроэнтерология",
    дерматолог: "дерматология",
    офтальмолог: "офтальмология",
    отоларинголог: "отоларингология",
    стоматолог: "стоматология",
    травматолог: "травматология",
    пульмонолог: "пульмонология",
    аллерголог: "аллергология",
  };

  const recommendedSpecializations: string[] = [];
  for (const [keyword, spec] of Object.entries(specKeywords)) {
    if (analysis.toLowerCase().includes(keyword)) {
      recommendedSpecializations.push(spec);
    }
  }

  return {
    analysis,
    recommendedSpecializations: recommendedSpecializations.length > 0 ? recommendedSpecializations : ["терапия"],
    disclaimer:
      "Это предварительная информация, а не медицинский диагноз. Обязательно обратитесь к врачу для точной диагностики и лечения.",
  };
}
