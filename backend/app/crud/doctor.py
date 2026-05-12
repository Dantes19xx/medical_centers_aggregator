from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.doctor import Doctor
from app.models.clinic import Clinic
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.utils.pagination import paginate
from typing import Optional, List
from uuid import UUID
import datetime


def get_doctor(db: Session, doctor_id: UUID) -> Optional[Doctor]:
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def get_doctors(
    db: Session,
    page: int = 1,
    limit: int = 20,
    specialty: Optional[str] = None,
    clinic_id: Optional[UUID] = None,
    city: Optional[str] = None,
    rating_min: Optional[float] = None,
    price_max: Optional[float] = None,
    search: Optional[str] = None,
) -> dict:
    query = db.query(Doctor)

    if specialty:
        query = query.filter(Doctor.specialty.ilike(f"%{specialty}%"))

    if clinic_id:
        query = query.filter(Doctor.clinic_id == clinic_id)

    if city:
        query = query.join(Clinic, Clinic.id == Doctor.clinic_id).filter(
            Clinic.city.ilike(f"%{city}%")
        )

    if rating_min is not None:
        query = query.filter(Doctor.rating >= rating_min)

    if price_max is not None:
        query = query.filter(Doctor.consultation_price <= price_max)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Doctor.first_name.ilike(search_term),
                Doctor.last_name.ilike(search_term),
                Doctor.specialty.ilike(search_term),
                Doctor.bio.ilike(search_term),
            )
        )

    query = query.order_by(Doctor.rating.desc(), Doctor.last_name)
    return paginate(query, page, limit)


def get_doctors_by_clinic(db: Session, clinic_id: UUID, page: int = 1, limit: int = 20) -> dict:
    query = db.query(Doctor).filter(Doctor.clinic_id == clinic_id).order_by(Doctor.last_name)
    return paginate(query, page, limit)


def get_specialties(db: Session) -> List[str]:
    results = db.query(Doctor.specialty).distinct().order_by(Doctor.specialty).all()
    return [r[0] for r in results if r[0]]


def create_doctor(db: Session, doctor_in: DoctorCreate) -> Doctor:
    db_doctor = Doctor(**doctor_in.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def update_doctor(db: Session, db_doctor: Doctor, doctor_update: DoctorUpdate) -> Doctor:
    update_data = doctor_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_doctor, field, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def update_doctor_rating(db: Session, doctor_id: UUID) -> None:
    from app.models.review import Review
    result = db.query(
        func.avg(Review.rating).label("avg_rating"),
        func.count(Review.id).label("count"),
    ).filter(Review.doctor_id == doctor_id).first()

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor:
        doctor.rating = round(float(result.avg_rating or 0), 2)
        doctor.reviews_count = result.count or 0
        db.commit()


def get_available_slots(
    db: Session,
    doctor_id: UUID,
    date: datetime.date,
) -> List[str]:
    from app.models.appointment import Appointment, AppointmentStatus

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return []

    clinic = db.query(Clinic).filter(Clinic.id == doctor.clinic_id).first()
    if not clinic or not clinic.working_hours:
        return []

    day_map = {
        0: "mon",
        1: "tue",
        2: "wed",
        3: "thu",
        4: "fri",
        5: "sat",
        6: "sun",
    }
    day_key = day_map.get(date.weekday())
    day_hours = clinic.working_hours.get(day_key)

    if not day_hours:
        return []

    open_str = day_hours.get("open")
    close_str = day_hours.get("close")
    if not open_str or not close_str:
        return []

    try:
        open_h, open_m = map(int, open_str.split(":"))
        close_h, close_m = map(int, close_str.split(":"))
    except (ValueError, AttributeError):
        return []

    open_time = datetime.time(open_h, open_m)
    close_time = datetime.time(close_h, close_m)

    # Generate slots every 30 minutes
    slots = []
    current = datetime.datetime.combine(date, open_time)
    end = datetime.datetime.combine(date, close_time)

    while current < end:
        slots.append(current.strftime("%H:%M"))
        current += datetime.timedelta(minutes=30)

    # Fetch already booked appointments (not cancelled)
    booked = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == date,
        Appointment.status.in_([
            AppointmentStatus.pending,
            AppointmentStatus.confirmed,
        ]),
    ).all()

    booked_times = {appt.appointment_time.strftime("%H:%M") for appt in booked}

    available = [slot for slot in slots if slot not in booked_times]
    return available
