"""Car API endpoints."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.api.dependencies import CarServiceDep, BookingServiceDep
from app.schemas.car import CarCategory, CarCreate, CarResponse, CarStatus, CarUpdate

router = APIRouter()


@router.get("", response_model=list[CarResponse])
async def list_cars(
    service: CarServiceDep,
    status: CarStatus | None = None,
    category: CarCategory | None = None,
):
    """List all cars with optional filters."""
    return await service.get_cars(status=status, category=category)


@router.get("/{car_id}", response_model=CarResponse)
async def get_car(car_id: str, service: CarServiceDep):
    """Get a car by ID."""
    car = await service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.post("", response_model=CarResponse, status_code=201)
async def create_car(data: CarCreate, service: CarServiceDep):
    """Create a new car."""
    return await service.create_car(data)


@router.put("/{car_id}", response_model=CarResponse)
async def update_car(car_id: str, data: CarUpdate, service: CarServiceDep):
    """Update a car."""
    car = await service.update_car(car_id, data)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.delete("/{car_id}", status_code=204)
async def delete_car(car_id: str, service: CarServiceDep):
    """Delete a car."""
    deleted = await service.delete_car(car_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")


@router.get("/{car_id}/availability")
async def check_availability(
    car_id: str,
    service: BookingServiceDep,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    """Check car availability for a date range."""
    return await service.check_availability(car_id, start_date, end_date)
