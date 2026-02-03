"""Shared API dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.booking import BookingRepository
from app.repositories.car import CarRepository
from app.repositories.customer import CustomerRepository
from app.services.booking import BookingService
from app.services.car import CarService
from app.services.customer import CustomerService

DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_car_service(db: DbSession) -> CarService:
    """Get car service dependency."""
    return CarService(CarRepository(db))


def get_customer_service(db: DbSession) -> CustomerService:
    """Get customer service dependency."""
    return CustomerService(CustomerRepository(db))


def get_booking_service(db: DbSession) -> BookingService:
    """Get booking service dependency."""
    return BookingService(
        booking_repository=BookingRepository(db),
        car_repository=CarRepository(db),
        customer_repository=CustomerRepository(db),
    )


CarServiceDep = Annotated[CarService, Depends(get_car_service)]
CustomerServiceDep = Annotated[CustomerService, Depends(get_customer_service)]
BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]
