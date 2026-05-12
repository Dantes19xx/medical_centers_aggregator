from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID
from decimal import Decimal


class ServiceBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(min_length=1, max_length=150)
    price_from: Optional[Decimal] = Field(None, ge=0)
    price_to: Optional[Decimal] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=1)
    is_available: bool = True


class ServiceCreate(ServiceBase):
    clinic_id: UUID


class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=150)
    price_from: Optional[Decimal] = Field(None, ge=0)
    price_to: Optional[Decimal] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=1)
    is_available: Optional[bool] = None


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    clinic_id: UUID
    name: str
    description: Optional[str] = None
    category: str
    price_from: Optional[Decimal] = None
    price_to: Optional[Decimal] = None
    duration_minutes: Optional[int] = None
    is_available: bool


class ServiceListOut(BaseModel):
    items: List[ServiceOut]
    total: int
    page: int
    limit: int
    pages: int
