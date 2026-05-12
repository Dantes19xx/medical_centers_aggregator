import uuid
from sqlalchemy import Column, String, Boolean, Integer, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(150), nullable=False, index=True)
    price_from = Column(Numeric(10, 2), nullable=True)
    price_to = Column(Numeric(10, 2), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)

    clinic = relationship("Clinic", back_populates="services")
    appointments = relationship("Appointment", back_populates="service")
