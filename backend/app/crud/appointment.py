from sqlalchemy.orm import Session
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.appointment import AppointmentCreate
from app.utils.pagination import paginate
from typing import Optional
from uuid import UUID


def get_appointment(db: Session, appointment_id: UUID) -> Optional[Appointment]:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_appointments_by_user(
    db: Session,
    user_id: UUID,
    page: int = 1,
    limit: int = 20,
) -> dict:
    query = db.query(Appointment).filter(Appointment.user_id == user_id).order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc(),
    )
    return paginate(query, page, limit)


def create_appointment(
    db: Session,
    appt_in: AppointmentCreate,
    user_id: Optional[UUID] = None,
) -> Appointment:
    db_appt = Appointment(
        user_id=user_id,
        doctor_id=appt_in.doctor_id,
        clinic_id=appt_in.clinic_id,
        service_id=appt_in.service_id,
        appointment_date=appt_in.appointment_date,
        appointment_time=appt_in.appointment_time,
        patient_name=appt_in.patient_name,
        patient_phone=appt_in.patient_phone,
        patient_email=appt_in.patient_email,
        notes=appt_in.notes,
        status=AppointmentStatus.pending,
    )
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


def cancel_appointment(db: Session, db_appt: Appointment) -> Appointment:
    db_appt.status = AppointmentStatus.cancelled
    db.commit()
    db.refresh(db_appt)
    return db_appt
