from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.utils.pagination import paginate
from typing import Optional, List
from uuid import UUID


def get_service(db: Session, service_id: UUID) -> Optional[Service]:
    return db.query(Service).filter(Service.id == service_id).first()


def get_services(
    db: Session,
    page: int = 1,
    limit: int = 20,
    clinic_id: Optional[UUID] = None,
    category: Optional[str] = None,
    price_max: Optional[float] = None,
    search: Optional[str] = None,
) -> dict:
    query = db.query(Service)

    if clinic_id:
        query = query.filter(Service.clinic_id == clinic_id)

    if category:
        query = query.filter(Service.category.ilike(f"%{category}%"))

    if price_max is not None:
        query = query.filter(Service.price_from <= price_max)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Service.name.ilike(search_term),
                Service.description.ilike(search_term),
            )
        )

    query = query.order_by(Service.category, Service.name)
    return paginate(query, page, limit)


def get_services_by_clinic(db: Session, clinic_id: UUID, page: int = 1, limit: int = 20) -> dict:
    query = db.query(Service).filter(Service.clinic_id == clinic_id).order_by(Service.category, Service.name)
    return paginate(query, page, limit)


def get_categories(db: Session) -> List[str]:
    results = db.query(Service.category).distinct().order_by(Service.category).all()
    return [r[0] for r in results if r[0]]


def create_service(db: Session, service_in: ServiceCreate) -> Service:
    db_service = Service(**service_in.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(db: Session, db_service: Service, service_update: ServiceUpdate) -> Service:
    update_data = service_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_service, field, value)
    db.commit()
    db.refresh(db_service)
    return db_service
