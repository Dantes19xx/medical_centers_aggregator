from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.database import get_db
from app.schemas.review import ReviewCreate, ReviewOut, ReviewListOut
from app.crud import clinic as clinic_crud
from app.crud import doctor as doctor_crud
from app.utils.auth import get_current_user
from app.models.user import User
from app.models.review import Review
from app.utils.pagination import paginate

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if review_in.clinic_id is None and review_in.doctor_id is None:
        raise HTTPException(
            status_code=400,
            detail="Either clinic_id or doctor_id must be provided",
        )

    if review_in.clinic_id:
        clinic = clinic_crud.get_clinic(db, review_in.clinic_id)
        if not clinic:
            raise HTTPException(status_code=404, detail="Clinic not found")

    if review_in.doctor_id:
        doctor = doctor_crud.get_doctor(db, review_in.doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

    db_review = Review(
        user_id=current_user.id,
        clinic_id=review_in.clinic_id,
        doctor_id=review_in.doctor_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # Update aggregate ratings
    if review_in.clinic_id:
        clinic_crud.update_clinic_rating(db, review_in.clinic_id)
    if review_in.doctor_id:
        doctor_crud.update_doctor_rating(db, review_in.doctor_id)

    return db_review


@router.get("/", response_model=ReviewListOut)
def list_reviews(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    clinic_id: Optional[UUID] = Query(None),
    doctor_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Review)
    if clinic_id:
        query = query.filter(Review.clinic_id == clinic_id)
    if doctor_id:
        query = query.filter(Review.doctor_id == doctor_id)
    query = query.order_by(Review.created_at.desc())
    return paginate(query, page, limit)
