"""API v1 router aggregating all routes."""

from fastapi import APIRouter

from app.api.v1 import cars, customers, bookings

router = APIRouter(prefix="/api/v1")

router.include_router(cars.router, prefix="/cars", tags=["Cars"])
router.include_router(customers.router, prefix="/customers", tags=["Customers"])
router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
