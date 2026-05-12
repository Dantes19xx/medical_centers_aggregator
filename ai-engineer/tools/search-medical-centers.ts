import { Tool } from "./index";

const BACKEND_API_BASE_URL =
  process.env.BACKEND_API_BASE_URL || "http://localhost:8000/api/v1";

type PaginatedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
};

type BackendDoctor = {
  id: string;
  clinic_id: string;
  clinic_name?: string;
  first_name: string;
  last_name: string;
  patronymic?: string | null;
  specialty: string;
  experience_years?: number | null;
  rating?: number | null;
  reviews_count?: number | null;
  consultation_price?: number | null;
  is_available?: boolean;
};

type BackendClinic = {
  id: string;
  name: string;
  address: string;
  city: string;
  district?: string | null;
  phone?: string | null;
  rating?: number | null;
  reviews_count?: number | null;
};

const SPECIALTY_ALIASES: Record<string, string> = {
  кардиология: "кардиолог",
  хирургия: "хирург",
  офтальмология: "офтальмолог",
  неврология: "невролог",
  педиатрия: "педиатр",
  стоматология: "стоматолог",
  дерматология: "дерматолог",
  гинекология: "гинеколог",
  ортопедия: "ортопед",
  терапия: "терапевт",
};

function normalizeSpecialty(specialization: string): string {
  const normalized = specialization.trim().toLowerCase();
  return SPECIALTY_ALIASES[normalized] || normalized;
}

function normalizeLocation(location: string): string {
  const normalized = location.trim().toLowerCase();
  if (!normalized || ["любой", "любая", "везде", "алматы"].includes(normalized)) {
    return "";
  }
  return location.trim();
}

async function getJson<T>(path: string, params: Record<string, string | number | undefined>) {
  const url = new URL(`${BACKEND_API_BASE_URL}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") {
      url.searchParams.set(key, String(value));
    }
  }

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Backend request failed: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

async function getOne<T>(path: string) {
  const response = await fetch(`${BACKEND_API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Backend request failed: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export const searchMedicalCenters: Tool = {
  name: "search_medical_centers",
  description:
    "Поиск врачей и медицинских центров в реальной базе backend по специализации, локации и рейтингу",
  parameters: {
    specialization: {
      type: "string",
      description: "Медицинская специализация (например, кардиология, терапия)",
    },
    location: {
      type: "string",
      description: "Город или район",
    },
    minRating: {
      type: "number",
      description: "Минимальный рейтинг от 1 до 5",
    },
    hasAvailableSlots: {
      type: "boolean",
      description: "Только с доступными слотами для записи",
    },
  },
  required: ["specialization"],
  execute: async (args) => {
    const specialization = normalizeSpecialty(String(args.specialization || ""));
    const location = normalizeLocation(String(args.location || ""));
    const minRating = Number(args.minRating || 0);

    const searchDoctors = (city: string, ratingMin?: number) =>
      getJson<PaginatedResponse<BackendDoctor>>("/doctors", {
        page: 1,
        limit: 10,
        specialty: specialization,
        city,
        rating_min: ratingMin || undefined,
      });

    let doctors = await searchDoctors(location, minRating);

    if (doctors.items.length === 0 && minRating > 0) {
      doctors = await searchDoctors(location);
    }

    if (doctors.items.length === 0 && location) {
      doctors = await searchDoctors("", minRating);
    }

    if (doctors.items.length === 0 && location && minRating > 0) {
      doctors = await searchDoctors("");
    }

    if (doctors.items.length === 0 && specialization) {
      doctors = await getJson<PaginatedResponse<BackendDoctor>>("/doctors", {
        page: 1,
        limit: 10,
        search: specialization,
      });
    }

    const clinicIds = [...new Set(doctors.items.map((doctor) => doctor.clinic_id))];
    const clinics = await Promise.all(
      clinicIds.map((clinicId) => getOne<BackendClinic>(`/clinics/${clinicId}`))
    );

    return {
      success: true,
      data: {
        doctors: doctors.items,
        clinics,
      },
      meta: {
        doctorsCount: doctors.items.length,
        clinicsCount: clinics.length,
        normalizedSpecialty: specialization,
        requestedLocation: location,
        backendApiBaseUrl: BACKEND_API_BASE_URL,
      },
    };
  },
};
