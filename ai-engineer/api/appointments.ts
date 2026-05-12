import { Router } from "express";
import { db } from "../db";

const router = Router();

router.get("/", async (_req, res) => {
  try {
    const appointments = await db.getAppointments();
    res.json({ success: true, data: appointments });
  } catch (error) {
    res.status(500).json({ success: false, error: "Ошибка получения записей" });
  }
});

export { router as appointmentsRouter };
