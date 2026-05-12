from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.clinic import Clinic
from app.models.doctor import Doctor
from app.schemas.clinic import ClinicCreate, ClinicUpdate
from app.utils.pagination import paginate
from typing import Optional
from uuid import UUID


def get_clinic(db: Session, clinic_id: UUID) -> Optional[Clinic]:
    return db.query(Clinic).filter(Clinic.id == clinic_id).first()


def get_clinics(
    db: Session,
    page: int = 1,
    limit: int = 20,
    city: Optional[str] = None,
    district: Optional[str] = None,
    specialty: Optional[str] = None,
    rating_min: Optional[float] = None,
    search: Optional[str] = None,
) -> dict:
    query = db.query(Clinic)

    if city:
        query = query.filter(Clinic.city.ilike(f"%{city}%"))

    if district:
        query = query.filter(Clinic.district.ilike(f"%{district}%"))

    if specialty:
        # Join with doctors to find clinics that have doctors with matching specialty
        query = query.join(Doctor, Doctor.clinic_id == Clinic.id).filter(
            Doctor.specialty.ilike(f"%{specialty}%")
        ).distinct()

    if rating_min is not None:
        query = query.filter(Clinic.rating >= rating_min)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Clinic.name.ilike(search_term),
                Clinic.description.ilike(search_term),
            )
        )

    query = query.order_by(Clinic.rating.desc(), Clinic.name)
    return paginate(query, page, limit)


def create_clinic(db: Session, clinic_in: ClinicCreate) -> Clinic:
    db_clinic = Clinic(**clinic_in.model_dump())
    db.add(db_clinic)
    db.commit()
    db.refresh(db_clinic)
    return db_clinic


def update_clinic(db: Session, db_clinic: Clinic, clinic_update: ClinicUpdate) -> Clinic:
    update_data = clinic_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_clinic, field, value)
    db.commit()
    db.refresh(db_clinic)
    return db_clinic


def delete_clinic(db: Session, db_clinic: Clinic) -> None:
    db.delete(db_clinic)
    db.commit()


def update_clinic_rating(db: Session, clinic_id: UUID) -> None:
    from app.models.review import Review
    result = db.query(
        func.avg(Review.rating).label("avg_rating"),
        func.count(Review.id).label("count"),
    ).filter(Review.clinic_id == clinic_id).first()

    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if clinic:
        clinic.rating = round(float(result.avg_rating or 0), 2)
        clinic.reviews_count = result.count or 0
        db.commit()
