import { Tool } from "./index";
import { db } from "../db";

export const getDoctorSchedule: Tool = {
  name: "get_doctor_schedule",
  description: "Получение расписания врача на указанную дату",
  parameters: {
    doctorId: {
      type: "string",
      description: "ID врача",
    },
    date: {
      type: "string",
      description: "Дата в формате YYYY-MM-DD",
    },
  },
  execute: async (args) => {
    const doctorId = String(args.doctorId || "");
    const date = String(args.date || "");

    if (!doctorId || !date) {
      return {
        success: false,
        error: "Требуются doctorId и date",
      };
    }

    const schedule = await db.getDoctorSchedule(doctorId, date);

    return {
      success: true,
      data: schedule,
    };
  },
};
