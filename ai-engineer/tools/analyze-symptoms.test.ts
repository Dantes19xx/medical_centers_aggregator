import { analyzeSymptoms } from "./analyze-symptoms";

describe("analyzeSymptoms tool", () => {
  it("should recommend cardiology for heart symptoms", async () => {
    const result = await analyzeSymptoms.execute({
      symptoms: "Болит сердце и повышенное давление",
    });

    expect(result.success).toBe(true);
    expect((result as any).data.possibleSpecializations).toContain("кардиология");
    expect((result as any).data.recommendedDoctors).toContain("Кардиолог");
    expect((result as any).data.disclaimer).toContain("не медицинский диагноз");
  });

  it("should recommend neurology for headache", async () => {
    const result = await analyzeSymptoms.execute({
      symptoms: "Головная боль и мигрень",
    });

    expect(result.success).toBe(true);
    expect((result as any).data.possibleSpecializations).toContain("неврология");
  });

  it("should require symptoms", async () => {
    const result = await analyzeSymptoms.execute({});

    expect(result.success).toBe(false);
    expect((result as any).error).toContain("Опишите");
  });

  it("should default to therapy if no match", async () => {
    const result = await analyzeSymptoms.execute({
      symptoms: "Общая слабость",
    });

    expect(result.success).toBe(true);
    expect((result as any).data.possibleSpecializations).toContain("терапия");
  });
});
