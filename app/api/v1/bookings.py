"""Booking API endpoints."""

from fastapi import APIRouter, HTTPException

from app.api.dependencies import BookingServiceDep
from app.schemas.booking import BookingCreate, BookingResponse, BookingStatus

router = APIRouter()


@router.get("", response_model=list[BookingResponse])
async def list_bookings(
    service: BookingServiceDep,
    status: BookingStatus | None = None,
    car_id: str | None = None,
    customer_id: str | None = None,
):
    """List all bookings with optional filters."""
    return await service.get_bookings(status=status, car_id=car_id, customer_id=customer_id)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: str, service: BookingServiceDep):
    """Get a booking by ID."""
    booking = await service.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("", response_model=BookingResponse, status_code=201)
async def create_booking(data: BookingCreate, service: BookingServiceDep):
    """Create a new booking (reservation)."""
    return await service.create_booking(data)


@router.post("/{booking_id}/pickup", response_model=BookingResponse)
async def pickup_car(booking_id: str, service: BookingServiceDep):
    """Start rental (reserved -> active)."""
    booking = await service.pickup_car(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/{booking_id}/return", response_model=BookingResponse)
async def return_car(booking_id: str, service: BookingServiceDep):
    """Complete rental (active -> completed)."""
    booking = await service.return_car(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(booking_id: str, service: BookingServiceDep):
    """Cancel a booking."""
    booking = await service.cancel_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
