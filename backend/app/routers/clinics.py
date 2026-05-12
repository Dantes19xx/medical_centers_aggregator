from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.database import get_db
from app.schemas.clinic import ClinicCreate, ClinicUpdate, ClinicOut, ClinicListOut
from app.schemas.doctor import DoctorListOut
from app.schemas.service import ServiceListOut
from app.schemas.review import ReviewListOut
from app.crud import clinic as clinic_crud
from app.crud import doctor as doctor_crud
from app.crud import service as service_crud
from app.utils.auth import get_current_admin_user
from app.models.user import User
from app.models.review import Review
from app.utils.pagination import paginate

router = APIRouter(prefix="/clinics", tags=["clinics"])


@router.get("/", response_model=ClinicListOut)
def list_clinics(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    city: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    rating: Optional[float] = Query(None, alias="rating_min"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    result = clinic_crud.get_clinics(
        db,
        page=page,
        limit=limit,
        city=city,
        district=district,
        specialty=specialty,
        rating_min=rating,
        search=search,
    )
    return result


@router.get("/{clinic_id}", response_model=ClinicOut)
def get_clinic(clinic_id: UUID, db: Session = Depends(get_db)):
    clinic = clinic_crud.get_clinic(db, clinic_id)
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return clinic


@router.get("/{clinic_id}/doctors", response_model=DoctorListOut)
def get_clinic_doctors(
    clinic_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    clinic = clinic_crud.get_clinic(db, clinic_id)
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return doctor_crud.get_doctors_by_clinic(db, clinic_id, page=page, limit=limit)


@router.get("/{clinic_id}/services", response_model=ServiceListOut)
def get_clinic_services(
    clinic_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    clinic = clinic_crud.get_clinic(db, clinic_id)
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return service_crud.get_services_by_clinic(db, clinic_id, page=page, limit=limit)


@router.get("/{clinic_id}/reviews", response_model=ReviewListOut)
def get_clinic_reviews(
    clinic_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    clinic = clinic_crud.get_clinic(db, clinic_id)
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    query = db.query(Review).filter(Review.clinic_id == clinic_id).order_by(Review.created_at.desc())
    return paginate(query, page, limit)


@router.post("/", response_model=ClinicOut, status_code=status.HTTP_201_CREATED)
def create_clinic(
    clinic_in: ClinicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    return clinic_crud.create_clinic(db, clinic_in)


@router.put("/{clinic_id}", response_model=ClinicOut)
def update_clinic(
    clinic_id: UUID,
    clinic_update: ClinicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    clinic = clinic_crud.get_clinic(db, clinic_id)
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return clinic_crud.update_clinic(db, clinic, clinic_update)


@router.delete("/{clinic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clinic(
    clinic_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    clinic = clinic_crud.get_clinic(db, clinic_id)
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    clinic_crud.delete_clinic(db, clinic)
