import { Router } from "express";
import { orchestrateChat } from "../agents/orchestrator";
import { researchCenters } from "../agents/research-agent";
import { processBooking } from "../agents/booking-agent";
import { analyzeSymptomsWithAgent } from "../agents/symptom-agent";

const router = Router();

router.post("/chat", async (req, res) => {
  try {
    const { userId, message, history } = req.body;

    if (!userId || !message) {
      return res.status(400).json({
        success: false,
        error: "Требуются userId и message",
      });
    }

    const result = await orchestrateChat(userId, message, history);

    res.json({
      success: true,
      data: {
        response: result.response,
        toolCalls: result.toolCalls,
      },
    });
  } catch (error) {
    console.error("AI Chat Error:", error);
    res.status(500).json({
      success: false,
      error: "Ошибка обработки запроса",
    });
  }
});

router.post("/research", async (req, res) => {
  try {
    const { query, specialization, location } = req.body;

    if (!query) {
      return res.status(400).json({
        success: false,
        error: "Требуется query",
      });
    }

    const result = await researchCenters(query, specialization, location);

    res.json({
      success: true,
      data: result,
    });
  } catch (error) {
    console.error("Research Error:", error);
    res.status(500).json({
      success: false,
      error: "Ошибка исследования",
    });
  }
});

router.post("/book", async (req, res) => {
  try {
    const { centerId, doctorId, patientName, patientPhone, date, time } = req.body;

    if (!centerId || !doctorId || !patientName || !date || !time) {
      return res.status(400).json({
        success: false,
        error: "Не все обязательные поля заполнены",
      });
    }

    const result = await processBooking({
      centerId,
      doctorId,
      patientName,
      patientPhone,
      date,
      time,
    });

    res.json({
      success: result.success,
      data: result,
    });
  } catch (error) {
    console.error("Booking Error:", error);
    res.status(500).json({
      success: false,
      error: "Ошибка бронирования",
    });
  }
});

router.post("/symptoms", async (req, res) => {
  try {
    const { symptoms, age, gender } = req.body;

    if (!symptoms) {
      return res.status(400).json({
        success: false,
        error: "Требуется описание симптомов",
      });
    }

    const result = await analyzeSymptomsWithAgent({ symptoms, age, gender });

    res.json({
      success: true,
      data: result,
    });
  } catch (error) {
    console.error("Symptom Analysis Error:", error);
    res.status(500).json({
      success: false,
      error: "Ошибка анализа симптомов",
    });
  }
});

export { router as aiChatRouter };
