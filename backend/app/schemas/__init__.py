"""Pydantic schemas for request/response validation."""

from app.schemas.car import (
    CarCategory,
    CarCreate,
    CarResponse,
    CarStatus,
    CarUpdate,
)
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingStatus,
    BookingUpdate,
)

__all__ = [
    "CarCategory",
    "CarStatus",
    "CarCreate",
    "CarUpdate",
    "CarResponse",
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "BookingStatus",
    "BookingCreate",
    "BookingUpdate",
    "BookingResponse",
]
