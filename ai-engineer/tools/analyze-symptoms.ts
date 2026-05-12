import { Tool } from "./index";

export const analyzeSymptoms: Tool = {
  name: "analyze_symptoms",
  description:
    "Первичный анализ симптомов пользователя для подбора подходящей специализации. НЕ предоставляет медицинский диагноз.",
  parameters: {
    symptoms: {
      type: "string",
      description: "Описание симптомов пользователя",
    },
    age: {
      type: "number",
      description: "Возраст пациента",
    },
    gender: {
      type: "string",
      description: "Пол пациента",
      enum: ["male", "female", "other"],
    },
  },
  execute: async (args) => {
    const symptoms = String(args.symptoms || "").toLowerCase();
    const age = Number(args.age || 0);
    const gender = String(args.gender || "other");

    if (!symptoms) {
      return {
        success: false,
        error: "Опишите симптомы",
      };
    }

    const keywords: Record<string, string[]> = {
      сердц: ["кардиология", "Кардиолог"],
      давлен: ["кардиология", "Терапевт"],
      груд: ["кардиология", "Терапевт"],
      голов: ["неврология", "Невролог"],
      мигрен: ["неврология", "Невролог"],
      живот: ["гастроэнтерология", "Гастроэнтеролог"],
      желуд: ["гастроэнтерология", "Гастроэнтеролог"],
      кож: ["дерматология", "Дерматолог"],
      сып: ["дерматология", "Дерматолог"],
      глаз: ["офтальмология", "Офтальмолог"],
      зрен: ["офтальмология", "Офтальмолог"],
      ухо: ["отоларингология", "Отоларинголог"],
      горл: ["отоларингология", "Отоларинголог"],
      нос: ["отоларингология", "Отоларинголог"],
      зуб: ["стоматология", "Стоматолог"],
      сустав: ["травматология", "Травматолог"],
      кост: ["травматология", "Травматолог"],
      позвоночн: ["травматология", "Травматолог"],
      дыхан: ["пульмонология", "Пульмонолог"],
      кашел: ["пульмонология", "Пульмонолог"],
      аллерг: ["аллергология", "Аллерголог"],
    };

    const matchedSpecializations: string[] = [];
    const matchedDoctors: string[] = [];

    for (const [keyword, [spec, doctor]] of Object.entries(keywords)) {
      if (symptoms.includes(keyword)) {
        if (!matchedSpecializations.includes(spec)) {
          matchedSpecializations.push(spec);
          matchedDoctors.push(doctor);
        }
      }
    }

    return {
      success: true,
      data: {
        possibleSpecializations: matchedSpecializations.length > 0 ? matchedSpecializations : ["терапия"],
        recommendedDoctors: matchedDoctors.length > 0 ? matchedDoctors : ["Терапевт"],
        disclaimer:
          "Это предварительная рекомендация, а не медицинский диагноз. Обратитесь к врачу для постановки точного диагноза.",
        age,
        gender,
      },
    };
  },
};
