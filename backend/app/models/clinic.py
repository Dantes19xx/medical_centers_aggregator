import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    logo_url = Column(String(500), nullable=True)
    photos = Column(ARRAY(String), nullable=True, default=list)
    working_hours = Column(JSON, nullable=True)
    rating = Column(Float, default=0.0, nullable=False)
    reviews_count = Column(Integer, default=0, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    doctors = relationship("Doctor", back_populates="clinic", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="clinic", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="clinic")
    reviews = relationship("Review", back_populates="clinic")
