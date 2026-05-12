import apiClient from './client';
import type { Doctor, Review, PaginatedResponse } from '../types';

export interface DoctorsParams {
  page?: number;
  limit?: number;
  specialty?: string;
  clinic_id?: number;
  experience_min?: number;
  price_max?: number;
  rating?: number;
}

export const getDoctors = (params?: DoctorsParams) =>
  apiClient.get<PaginatedResponse<Doctor>>('/doctors', { params }).then(r => r.data);

export const getDoctor = (id: number) =>
  apiClient.get<Doctor>(`/doctors/${id}`).then(r => r.data);

export const getDoctorReviews = (id: number) =>
  apiClient.get<Review[]>(`/doctors/${id}/reviews`).then(r => r.data);

export const getDoctorSlots = (id: number, date: string) =>
  apiClient.get<string[]>(`/doctors/${id}/slots`, { params: { date } }).then(r => r.data);

export const getSpecialties = () =>
  apiClient.get<string[]>('/doctors/specialties').then(r => r.data);
