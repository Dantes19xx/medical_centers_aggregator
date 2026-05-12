from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentOut, AppointmentListOut
from app.crud import appointment as appt_crud
from app.utils.auth import get_current_user, get_optional_current_user
from app.models.user import User, UserRole

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appt_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    user_id = current_user.id if current_user else None
    return appt_crud.create_appointment(db, appt_in, user_id=user_id)


@router.get("/", response_model=AppointmentListOut)
def list_my_appointments(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return appt_crud.get_appointments_by_user(db, current_user.id, page=page, limit=limit)


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appt = appt_crud.get_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if current_user.role != UserRole.admin and appt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return appt


@router.patch("/{appointment_id}/cancel", response_model=AppointmentOut)
def cancel_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appt = appt_crud.get_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if current_user.role != UserRole.admin and appt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    from app.models.appointment import AppointmentStatus
    if appt.status == AppointmentStatus.cancelled:
        raise HTTPException(status_code=400, detail="Appointment is already cancelled")
    if appt.status == AppointmentStatus.completed:
        raise HTTPException(status_code=400, detail="Cannot cancel a completed appointment")
    return appt_crud.cancel_appointment(db, appt)
