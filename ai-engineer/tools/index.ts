import { searchMedicalCenters } from "./search-medical-centers";
import { bookAppointment } from "./book-appointment";
import { getDoctorSchedule } from "./get-doctor-schedule";
import { analyzeSymptoms } from "./analyze-symptoms";
import { sendNotification } from "./send-notification";

export interface Tool {
  name: string;
  description: string;
  parameters: Record<string, { type: string; description: string; enum?: string[] }>;
  execute: (args: Record<string, unknown>) => Promise<unknown>;
}

export const tools: Tool[] = [
  searchMedicalCenters,
  bookAppointment,
  getDoctorSchedule,
  analyzeSymptoms,
  sendNotification,
];

export const toolsMap = new Map(tools.map((t) => [t.name, t]));
