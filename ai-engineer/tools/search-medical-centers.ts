import { Tool } from "./index";
import { db } from "../db";

export const searchMedicalCenters: Tool = {
  name: "search_medical_centers",
  description:
    "Поиск медицинских центров по специализации, локации, рейтингу и доступности записи",
  parameters: {
    specialization: {
      type: "string",
      description: "Медицинская специализация (например, кардиология, терапия)",
    },
    location: {
      type: "string",
      description: "Город или район",
    },
    minRating: {
      type: "number",
      description: "Минимальный рейтинг от 1 до 5",
    },
    hasAvailableSlots: {
      type: "boolean",
      description: "Только с доступными слотами для записи",
    },
  },
  execute: async (args) => {
    const specialization = String(args.specialization || "").toLowerCase();
    const location = String(args.location || "").toLowerCase();
    const minRating = Number(args.minRating || 0);
    const hasAvailableSlots = Boolean(args.hasAvailableSlots);

    const centers = await db.getMedicalCenters({
      specialization,
      location,
      minRating,
      hasAvailableSlots,
    });

    return {
      success: true,
      data: centers,
      meta: { count: centers.length },
    };
  },
};
