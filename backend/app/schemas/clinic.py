from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class ClinicBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    address: str = Field(min_length=1, max_length=500)
    city: str = Field(min_length=1, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = None
    website: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=500)
    photos: Optional[List[str]] = None
    working_hours: Optional[Dict[str, Any]] = None
    is_verified: bool = False


class ClinicCreate(ClinicBase):
    pass


class ClinicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = None
    website: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=500)
    photos: Optional[List[str]] = None
    working_hours: Optional[Dict[str, Any]] = None
    is_verified: Optional[bool] = None


class ClinicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: Optional[str] = None
    address: str
    city: str
    district: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    photos: Optional[List[str]] = None
    working_hours: Optional[Dict[str, Any]] = None
    rating: float
    reviews_count: int
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class ClinicListOut(BaseModel):
    items: List[ClinicOut]
    total: int
    page: int
    limit: int
    pages: int
