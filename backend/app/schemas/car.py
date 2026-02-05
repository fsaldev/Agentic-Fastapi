"""Pydantic schemas for Car."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class CarCategory(str, Enum):
    """Car category enumeration."""

    ECONOMY = "economy"
    STANDARD = "standard"
    LUXURY = "luxury"
    SUV = "suv"


class CarStatus(str, Enum):
    """Car status enumeration."""

    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"


class CarBase(BaseModel):
    """Base schema for Car with common fields."""

    make: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1900, le=2100)
    license_plate: str = Field(..., min_length=1, max_length=20)
    daily_rate: float = Field(..., gt=0)
    category: CarCategory = CarCategory.STANDARD


class CarCreate(CarBase):
    """Schema for creating a new car."""

    pass


class CarUpdate(BaseModel):
    """Schema for updating a car. All fields optional."""

    make: str | None = Field(None, min_length=1, max_length=100)
    model: str | None = Field(None, min_length=1, max_length=100)
    year: int | None = Field(None, ge=1900, le=2100)
    license_plate: str | None = Field(None, min_length=1, max_length=20)
    daily_rate: float | None = Field(None, gt=0)
    category: CarCategory | None = None
    status: CarStatus | None = None


class CarResponse(CarBase):
    """Schema for car response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    status: CarStatus
    created_at: datetime
