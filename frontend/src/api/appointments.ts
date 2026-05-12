import apiClient from './client';
import type { Appointment } from '../types';

export interface CreateAppointmentDto {
  doctor_id: number;
  clinic_id: number;
  service_id?: number;
  appointment_date: string;
  appointment_time: string;
  patient_name: string;
  patient_phone: string;
  patient_email: string;
  notes?: string;
}

export const createAppointment = (data: CreateAppointmentDto) =>
  apiClient.post<Appointment>('/appointments', data).then(r => r.data);

export const getMyAppointments = () =>
  apiClient.get<Appointment[]>('/appointments').then(r => r.data);

export const cancelAppointment = (id: number) =>
  apiClient.patch<Appointment>(`/appointments/${id}/cancel`).then(r => r.data);
