export interface Clinic {
  id: number;
  name: string;
  description: string;
  address: string;
  city: string;
  district: string;
  phone: string;
  email: string;
  logo_url: string;
  photos: string[];
  rating: number;
  reviews_count: number;
  is_verified: boolean;
  working_hours: Record<string, string>;
}

export interface Doctor {
  id: number;
  clinic_id: number;
  clinic_name: string;
  first_name: string;
  last_name: string;
  patronymic: string;
  specialty: string;
  experience_years: number;
  education: string;
  bio: string;
  photo_url: string;
  rating: number;
  reviews_count: number;
  consultation_price: number;
  is_available: boolean;
}

export interface Service {
  id: number;
  clinic_id: number;
  name: string;
  description: string;
  category: string;
  price_from: number;
  price_to: number;
  duration_minutes: number;
  is_available: boolean;
}

export interface Appointment {
  id: number;
  doctor_id: number;
  clinic_id: number;
  service_id?: number;
  appointment_date: string;
  appointment_time: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  patient_name: string;
  patient_phone: string;
  patient_email: string;
  notes?: string;
}

export interface Review {
  id: number;
  user_id: number;
  clinic_id?: number;
  doctor_id?: number;
  rating: number;
  comment: string;
  created_at: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  phone: string;
  role: 'patient' | 'admin';
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  suggestions: string[];
  cards: Array<{
    type: 'clinic' | 'doctor' | 'service';
    id: number;
    name: string;
    [key: string]: unknown;
  }>;
}
