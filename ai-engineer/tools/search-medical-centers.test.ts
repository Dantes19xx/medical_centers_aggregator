import { searchMedicalCenters } from "./search-medical-centers";

describe("searchMedicalCenters tool", () => {
  it("should return centers by specialization", async () => {
    const result = await searchMedicalCenters.execute({
      specialization: "кардиология",
    });

    expect(result.success).toBe(true);
    expect(Array.isArray((result as any).data)).toBe(true);
    expect((result as any).data.length).toBeGreaterThan(0);
    expect((result as any).meta.count).toBeGreaterThan(0);
  });

  it("should filter by location", async () => {
    const result = await searchMedicalCenters.execute({
      location: "Москва",
    });

    expect(result.success).toBe(true);
    expect((result as any).data.every((c: any) => c.city === "Москва")).toBe(true);
  });

  it("should filter by minRating", async () => {
    const result = await searchMedicalCenters.execute({
      minRating: 4.5,
    });

    expect(result.success).toBe(true);
    expect((result as any).data.every((c: any) => c.rating >= 4.5)).toBe(true);
  });

  it("should return empty array for unknown specialization", async () => {
    const result = await searchMedicalCenters.execute({
      specialization: "натуропатия",
    });

    expect(result.success).toBe(true);
    expect((result as any).data.length).toBe(0);
  });
});
