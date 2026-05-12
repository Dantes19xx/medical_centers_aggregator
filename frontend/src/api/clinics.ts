import apiClient from './client';
import type { Clinic, Doctor, Service, Review, PaginatedResponse } from '../types';

export interface ClinicsParams {
  page?: number;
  limit?: number;
  search?: string;
  city?: string;
  district?: string;
  specialty?: string;
  rating?: number;
}

export const getClinics = (params?: ClinicsParams) =>
  apiClient.get<PaginatedResponse<Clinic>>('/clinics', { params }).then(r => r.data);

export const getClinic = (id: number) =>
  apiClient.get<Clinic>(`/clinics/${id}`).then(r => r.data);

export const getClinicDoctors = (id: number) =>
  apiClient.get<Doctor[]>(`/clinics/${id}/doctors`).then(r => r.data);

export const getClinicServices = (id: number) =>
  apiClient.get<Service[]>(`/clinics/${id}/services`).then(r => r.data);

export const getClinicReviews = (id: number) =>
  apiClient.get<Review[]>(`/clinics/${id}/reviews`).then(r => r.data);
