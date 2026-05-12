from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import date
from app.database import get_db
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorOut, DoctorListOut
from app.schemas.review import ReviewListOut
from app.crud import doctor as doctor_crud
from app.utils.auth import get_current_admin_user
from app.models.user import User
from app.models.review import Review
from app.utils.pagination import paginate

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get("/specialties", response_model=List[str])
def get_specialties(db: Session = Depends(get_db)):
    return doctor_crud.get_specialties(db)


@router.get("/", response_model=DoctorListOut)
def list_doctors(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    specialty: Optional[str] = Query(None),
    clinic_id: Optional[UUID] = Query(None),
    city: Optional[str] = Query(None),
    rating_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return doctor_crud.get_doctors(
        db,
        page=page,
        limit=limit,
        specialty=specialty,
        clinic_id=clinic_id,
        city=city,
        rating_min=rating_min,
        price_max=price_max,
        search=search,
    )


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: UUID, db: Session = Depends(get_db)):
    doctor = doctor_crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.get("/{doctor_id}/reviews", response_model=ReviewListOut)
def get_doctor_reviews(
    doctor_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    doctor = doctor_crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    query = db.query(Review).filter(Review.doctor_id == doctor_id).order_by(Review.created_at.desc())
    return paginate(query, page, limit)


@router.get("/{doctor_id}/slots", response_model=List[str])
def get_doctor_slots(
    doctor_id: UUID,
    date: date = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
):
    doctor = doctor_crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    slots = doctor_crud.get_available_slots(db, doctor_id, date)
    return slots


@router.post("/", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor_in: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    return doctor_crud.create_doctor(db, doctor_in)


@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(
    doctor_id: UUID,
    doctor_update: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    doctor = doctor_crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor_crud.update_doctor(db, doctor, doctor_update)
