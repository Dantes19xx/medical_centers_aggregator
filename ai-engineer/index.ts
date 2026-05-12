import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { aiChatRouter } from "./api/ai-chat";
import { medicalCentersRouter } from "./api/medical-centers";
import { appointmentsRouter } from "./api/appointments";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

app.use("/api/ai", aiChatRouter);
app.use("/api/centers", medicalCentersRouter);
app.use("/api/appointments", appointmentsRouter);

app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "medical-aggregator-backend" });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

export default app;
