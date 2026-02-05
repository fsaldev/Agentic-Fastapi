"""Pydantic schemas for Booking."""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class BookingStatus(str, Enum):
    """Booking status enumeration."""

    RESERVED = "reserved"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BookingBase(BaseModel):
    """Base schema for Booking with common fields."""

    car_id: str
    customer_id: str
    start_date: date
    end_date: date


class BookingCreate(BookingBase):
    """Schema for creating a new booking."""

    pass


class BookingUpdate(BaseModel):
    """Schema for updating a booking. All fields optional."""

    start_date: date | None = None
    end_date: date | None = None


class BookingResponse(BookingBase):
    """Schema for booking response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    actual_return_date: date | None
    total_cost: float
    status: BookingStatus
    created_at: datetime
