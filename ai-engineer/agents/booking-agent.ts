import Anthropic from "@anthropic-ai/sdk";
import { db } from "../db";
import { v4 as uuidv4 } from "uuid";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || "",
});

export interface BookingRequest {
  centerId: string;
  doctorId: string;
  patientName: string;
  patientPhone: string;
  date: string;
  time: string;
}

export async function processBooking(
  request: BookingRequest
): Promise<{ success: boolean; message: string; appointmentId?: string }> {
  const schedule = await db.getDoctorSchedule(request.doctorId, request.date);
  if (!schedule.slots.includes(request.time)) {
    return {
      success: false,
      message: `Выбранное время ${request.time} недоступно. Доступные слоты: ${schedule.slots.join(", ")}`,
    };
  }

  const appointmentId = uuidv4();
  await db.createAppointment({
    id: appointmentId,
    ...request,
    status: "confirmed",
  });

  const systemPrompt = `
Ты — booking-agent медицинского агрегатора. Твоя задача — подтвердить запись
и дать пользователю чёткие инструкции.
`;

  const userPrompt = `
Запись подтверждена:
- ID записи: ${appointmentId}
- Пациент: ${request.patientName}
- Дата: ${request.date}
- Время: ${request.time}
- Врач: ${request.doctorId}
- Центр: ${request.centerId}

Составь дружелюбное подтверждение на русском языке.
`;

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    system: systemPrompt,
    messages: [{ role: "user", content: userPrompt }],
  });

  const message = response.content
    .filter((c) => c.type === "text")
    .map((c) => (c as Anthropic.TextBlock).text)
    .join(" ");

  return { success: true, message, appointmentId };
}
