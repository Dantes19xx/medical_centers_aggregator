from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from app.database import get_db
from app.schemas.service import ServiceOut, ServiceListOut
from app.crud import service as service_crud

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    return service_crud.get_categories(db)


@router.get("/", response_model=ServiceListOut)
def list_services(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    clinic_id: Optional[UUID] = Query(None),
    category: Optional[str] = Query(None),
    price_max: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return service_crud.get_services(
        db,
        page=page,
        limit=limit,
        clinic_id=clinic_id,
        category=category,
        price_max=price_max,
        search=search,
    )


@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: UUID, db: Session = Depends(get_db)):
    service = service_crud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service
