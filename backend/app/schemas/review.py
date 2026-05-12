from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ReviewCreate(BaseModel):
    clinic_id: Optional[UUID] = None
    doctor_id: Optional[UUID] = None
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

    def model_post_init(self, __context) -> None:
        if self.clinic_id is None and self.doctor_id is None:
            raise ValueError("Either clinic_id or doctor_id must be provided")


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    clinic_id: Optional[UUID] = None
    doctor_id: Optional[UUID] = None
    rating: int
    comment: Optional[str] = None
    is_moderated: bool
    created_at: datetime


class ReviewListOut(BaseModel):
    items: List[ReviewOut]
    total: int
    page: int
    limit: int
    pages: int
