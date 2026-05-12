import math
from typing import TypeVar, Generic, List, Type
from pydantic import BaseModel
from sqlalchemy.orm import Query

T = TypeVar("T")


def paginate(query: Query, page: int, limit: int) -> dict:
    """
    Apply pagination to a SQLAlchemy query.
    Returns a dict with items, total, page, limit, pages.
    """
    if page < 1:
        page = 1
    if limit < 1:
        limit = 1
    if limit > 100:
        limit = 100

    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages,
    }
