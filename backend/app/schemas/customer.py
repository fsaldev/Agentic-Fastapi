"""Pydantic schemas for Customer."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerBase(BaseModel):
    """Base schema for Customer with common fields."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=20)
    driver_license: str = Field(..., min_length=1, max_length=50)


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer."""

    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer. All fields optional."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, min_length=1, max_length=20)
    driver_license: str | None = Field(None, min_length=1, max_length=50)


class CustomerResponse(CustomerBase):
    """Schema for customer response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
