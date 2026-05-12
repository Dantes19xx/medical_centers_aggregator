import { Router } from "express";
import { db } from "../db";

const router = Router();

router.get("/", async (_req, res) => {
  try {
    const centers = await db.getMedicalCenters({});
    res.json({ success: true, data: centers });
  } catch (error) {
    res.status(500).json({ success: false, error: "Ошибка получения списка клиник" });
  }
});

router.get("/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const centers = await db.getMedicalCenters({});
    const center = centers.find((c) => c.id === id);

    if (!center) {
      return res.status(404).json({ success: false, error: "Клиника не найдена" });
    }

    res.json({ success: true, data: center });
  } catch (error) {
    res.status(500).json({ success: false, error: "Ошибка получения клиники" });
  }
});

export { router as medicalCentersRouter };
