import { Tool } from "./index";

export const sendNotification: Tool = {
  name: "send_notification",
  description: "Отправка уведомления пользователю (email, sms или push)",
  parameters: {
    userId: {
      type: "string",
      description: "ID пользователя",
    },
    type: {
      type: "string",
      description: "Тип уведомления",
      enum: ["email", "sms", "push"],
    },
    message: {
      type: "string",
      description: "Текст уведомления",
    },
  },
  execute: async (args) => {
    const userId = String(args.userId || "");
    const type = String(args.type || "push");
    const message = String(args.message || "");

    if (!userId || !message) {
      return {
        success: false,
        error: "Требуются userId и message",
      };
    }

    console.log(`[NOTIFICATION] ${type.toUpperCase()} to user ${userId}: ${message}`);

    return {
      success: true,
      data: {
        sent: true,
        type,
        userId,
        timestamp: new Date().toISOString(),
      },
    };
  },
};
