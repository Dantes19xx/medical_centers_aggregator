export interface MedicalCenter {
  id: string;
  name: string;
  address: string;
  city: string;
  rating: number;
  specializations: string[];
  doctors: Doctor[];
}

export interface Doctor {
  id: string;
  name: string;
  specialization: string;
  rating: number;
  schedule: Record<string, string[]>;
}

export interface Appointment {
  id: string;
  centerId: string;
  doctorId: string;
  patientName: string;
  patientPhone: string;
  date: string;
  time: string;
  status: "confirmed" | "cancelled" | "completed";
}

const centers: MedicalCenter[] = [
  {
    id: "c1",
    name: "Центральная клиника",
    address: "ул. Ленина, 10",
    city: "Москва",
    rating: 4.8,
    specializations: ["кардиология", "неврология", "терапия"],
    doctors: [
      {
        id: "d1",
        name: "Иванов А.П.",
        specialization: "Кардиолог",
        rating: 4.9,
        schedule: {
          "2026-05-13": ["09:00", "10:00", "11:00"],
          "2026-05-14": ["14:00", "15:00"],
        },
      },
      {
        id: "d2",
        name: "Петрова М.С.",
        specialization: "Терапевт",
        rating: 4.7,
        schedule: {
          "2026-05-13": ["10:00", "12:00", "16:00"],
        },
      },
    ],
  },
  {
    id: "c2",
    name: "Семейный доктор",
    address: "пр. Мира, 25",
    city: "Москва",
    rating: 4.5,
    specializations: ["терапия", "педиатрия", "гастроэнтерология"],
    doctors: [
      {
        id: "d3",
        name: "Сидоров К.В.",
        specialization: "Гастроэнтеролог",
        rating: 4.6,
        schedule: {
          "2026-05-13": ["09:30", "11:30"],
          "2026-05-15": ["10:00", "14:00"],
        },
      },
    ],
  },
  {
    id: "c3",
    name: "Клиника Здоровье",
    address: "ул. Гагарина, 5",
    city: "Санкт-Петербург",
    rating: 4.2,
    specializations: ["дерматология", "аллергология"],
    doctors: [
      {
        id: "d4",
        name: "Козлова Е.Д.",
        specialization: "Дерматолог",
        rating: 4.4,
        schedule: {
          "2026-05-13": ["10:00", "13:00", "15:00"],
        },
      },
    ],
  },
];

const appointments: Appointment[] = [];

export const db = {
  getMedicalCenters: async (filters: {
    specialization?: string;
    location?: string;
    minRating?: number;
    hasAvailableSlots?: boolean;
  }): Promise<MedicalCenter[]> => {
    return centers.filter((c) => {
      if (filters.specialization && !c.specializations.includes(filters.specialization)) return false;
      if (filters.location && !c.city.toLowerCase().includes(filters.location)) return false;
      if (filters.minRating && c.rating < filters.minRating) return false;
      if (filters.hasAvailableSlots && c.doctors.every((d) => Object.keys(d.schedule).length === 0)) return false;
      return true;
    });
  },

  getDoctorSchedule: async (doctorId: string, date: string): Promise<{ date: string; slots: string[] }> => {
    for (const center of centers) {
      const doctor = center.doctors.find((d) => d.id === doctorId);
      if (doctor) {
        return { date, slots: doctor.schedule[date] || [] };
      }
    }
    return { date, slots: [] };
  },

  createAppointment: async (appointment: Appointment): Promise<void> => {
    appointments.push(appointment);
  },

  getAppointments: async (): Promise<Appointment[]> => {
    return appointments;
  },
};
