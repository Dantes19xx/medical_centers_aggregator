import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Date, Time, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class AppointmentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, index=True)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id", ondelete="SET NULL"), nullable=True, index=True)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(SAEnum(AppointmentStatus), default=AppointmentStatus.pending, nullable=False)
    patient_name = Column(String(255), nullable=False)
    patient_phone = Column(String(50), nullable=False)
    patient_email = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    clinic = relationship("Clinic", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
