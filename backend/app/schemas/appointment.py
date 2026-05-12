from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date, time
from uuid import UUID
from app.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    doctor_id: UUID
    clinic_id: UUID
    service_id: Optional[UUID] = None
    appointment_date: date
    appointment_time: time
    patient_name: str = Field(min_length=1, max_length=255)
    patient_phone: str = Field(min_length=1, max_length=50)
    patient_email: Optional[str] = None
    notes: Optional[str] = None


class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: Optional[UUID] = None
    doctor_id: UUID
    clinic_id: UUID
    service_id: Optional[UUID] = None
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus
    patient_name: str
    patient_phone: str
    patient_email: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime


class AppointmentListOut(BaseModel):
    items: List[AppointmentOut]
    total: int
    page: int
    limit: int
    pages: int
