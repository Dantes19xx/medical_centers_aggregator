from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class DoctorBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    specialty: str = Field(min_length=1, max_length=150)
    experience_years: Optional[int] = Field(None, ge=0)
    education: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500)
    consultation_price: Optional[Decimal] = Field(None, ge=0)
    is_available: bool = True


class DoctorCreate(DoctorBase):
    clinic_id: UUID


class DoctorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    specialty: Optional[str] = Field(None, min_length=1, max_length=150)
    experience_years: Optional[int] = Field(None, ge=0)
    education: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500)
    consultation_price: Optional[Decimal] = Field(None, ge=0)
    is_available: Optional[bool] = None


class DoctorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    clinic_id: UUID
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    specialty: str
    experience_years: Optional[int] = None
    education: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    rating: float
    reviews_count: int
    consultation_price: Optional[Decimal] = None
    is_available: bool
    created_at: datetime


class DoctorListOut(BaseModel):
    items: List[DoctorOut]
    total: int
    page: int
    limit: int
    pages: int
