import { Tool } from "./index";
import { db } from "../db";
import { v4 as uuidv4 } from "uuid";

export const bookAppointment: Tool = {
  name: "book_appointment",
  description: "Запись пациента на приём к врачу в выбранный медицинский центр",
  parameters: {
    centerId: {
      type: "string",
      description: "ID медицинского центра",
    },
    doctorId: {
      type: "string",
      description: "ID врача",
    },
    patientName: {
      type: "string",
      description: "Имя пациента",
    },
    patientPhone: {
      type: "string",
      description: "Телефон пациента",
    },
    date: {
      type: "string",
      description: "Дата приёма в формате YYYY-MM-DD",
    },
    time: {
      type: "string",
      description: "Время приёма в формате HH:mm",
    },
  },
  execute: async (args) => {
    const centerId = String(args.centerId || "");
    const doctorId = String(args.doctorId || "");
    const patientName = String(args.patientName || "");
    const patientPhone = String(args.patientPhone || "");
    const date = String(args.date || "");
    const time = String(args.time || "");

    if (!centerId || !doctorId || !patientName || !date || !time) {
      return {
        success: false,
        error: "Не все обязательные поля заполнены",
        required: ["centerId", "doctorId", "patientName", "date", "time"],
      };
    }

    const appointmentId = uuidv4();
    await db.createAppointment({
      id: appointmentId,
      centerId,
      doctorId,
      patientName,
      patientPhone,
      date,
      time,
      status: "confirmed",
    });

    return {
      success: true,
      data: {
        appointmentId,
        status: "confirmed",
        message: `Запись подтверждена. ID: ${appointmentId}`,
      },
    };
  },
};
