"""Tests for Create Booking (reservation) endpoint."""

from datetime import date, timedelta

import pytest
from httpx import AsyncClient


BOOKINGS_URL = "/api/v1/bookings"
CARS_URL = "/api/v1/cars"
CUSTOMERS_URL = "/api/v1/customers"

SAMPLE_CAR = {
    "make": "Toyota",
    "model": "Camry",
    "year": 2024,
    "license_plate": "BKG-0001",
    "daily_rate": 50.00,
    "category": "standard",
}

SAMPLE_CUSTOMER = {
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice.smith@example.com",
    "phone": "+1234567890",
    "driver_license": "DL-999999",
}


def future_date(days_ahead: int) -> str:
    """Return an ISO-formatted date N days from today."""
    return (date.today() + timedelta(days=days_ahead)).isoformat()


@pytest.mark.asyncio
class TestCreateBooking:
    """Tests for POST /api/v1/bookings."""

    async def _create_car(self, client: AsyncClient, **overrides) -> dict:
        car = {**SAMPLE_CAR, **overrides}
        resp = await client.post(CARS_URL, json=car)
        return resp.json()

    async def _create_customer(self, client: AsyncClient, **overrides) -> dict:
        customer = {**SAMPLE_CUSTOMER, **overrides}
        resp = await client.post(CUSTOMERS_URL, json=customer)
        return resp.json()

    async def test_create_booking_success(self, client: AsyncClient):
        car = await self._create_car(client)
        customer = await self._create_customer(client)

        booking_data = {
            "car_id": car["id"],
            "customer_id": customer["id"],
            "start_date": future_date(1),
            "end_date": future_date(4),
        }
        response = await client.post(BOOKINGS_URL, json=booking_data)
        assert response.status_code == 201
        data = response.json()
        assert data["car_id"] == car["id"]
        assert data["customer_id"] == customer["id"]
        assert data["status"] == "reserved"
        assert data["total_cost"] == 150.00  # 3 days × $50
        assert "id" in data
        assert "created_at" in data

    async def test_create_booking_car_not_found(self, client: AsyncClient):
        customer = await self._create_customer(client)
        booking_data = {
            "car_id": "nonexistent-car-id",
            "customer_id": customer["id"],
            "start_date": future_date(1),
            "end_date": future_date(3),
        }
        response = await client.post(BOOKINGS_URL, json=booking_data)
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    async def test_create_booking_car_in_maintenance(self, client: AsyncClient):
        car = await self._create_car(client)
        customer = await self._create_customer(client)

        # Put car in maintenance
        await client.put(f"{CARS_URL}/{car['id']}", json={"status": "maintenance"})

        booking_data = {
            "car_id": car["id"],
            "customer_id": customer["id"],
            "start_date": future_date(1),
            "end_date": future_date(3),
        }
        response = await client.post(BOOKINGS_URL, json=booking_data)
        assert response.status_code == 400
        assert "maintenance" in response.json()["detail"]

    async def test_create_booking_customer_not_found(self, client: AsyncClient):
        car = await self._create_car(client)
        booking_data = {
            "car_id": car["id"],
            "customer_id": "nonexistent-customer-id",
            "start_date": future_date(1),
            "end_date": future_date(3),
        }
        response = await client.post(BOOKINGS_URL, json=booking_data)
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    async def test_create_booking_start_date_after_end_date(self, client: AsyncClient):
        car = await self._create_car(client)
        customer = await self._create_customer(client)
        booking_data = {
            "car_id": car["id"],
            "customer_id": customer["id"],
            "start_date": future_date(5),
            "end_date": future_date(2),
        }
        response = await client.post(BOOKINGS_URL, json=booking_data)
        assert response.status_code == 400
        assert "before end date" in response.json()["detail"]

    async def test_create_booking_start_date_equals_end_date(self, client: AsyncClient):
        car = await self._create_car(client)
        customer = await self._create_customer(client)
        same_date = future_date(3)
        booking_data = {
            "car_id": car["id"],
            "customer_id": customer["id"],
            "start_date": same_date,
            "end_date": same_date,
        }
        response = await client.post(BOOKINGS_URL, json=booking_data)
        assert response.status_code == 400
        assert "before end date" in response.json()["detail"]

    async def test_create_booking_start_date_in_past(self, client: AsyncClient):
        car = await self._create_car(client)
        customer = await self._create_customer(client)
        booking_data = {
            "car_id": car["id"],
            "customer_id": customer["id"],
            "start_date": (date.today() - timedelta(days=1)).isoformat(),
            "end_date": future_date(3),
        }
        response = await client.post(BOOKINGS_URL, json=booking_data)
        assert response.status_code == 400
        assert "past" in response.json()["detail"]

    async def test_create_booking_double_booking_prevented(self, client: AsyncClient):
        car = await self._create_car(client)
        customer = await self._create_customer(client)

        # First booking
        booking_data = {
            "car_id": car["id"],
            "customer_id": customer["id"],
            "start_date": future_date(1),
            "end_date": future_date(5),
        }
        resp = await client.post(BOOKINGS_URL, json=booking_data)
        assert resp.status_code == 201

        # Second booking with overlapping dates
        customer2 = await self._create_customer(client, email="bob@example.com")
        overlapping_data = {
            "car_id": car["id"],
            "customer_id": customer2["id"],
            "start_date": future_date(3),
            "end_date": future_date(7),
        }
        response = await client.post(BOOKINGS_URL, json=overlapping_data)
        assert response.status_code == 400
        assert "not available" in response.json()["detail"]

    async def test_create_booking_total_cost_calculation(self, client: AsyncClient):
        car = await self._create_car(client, daily_rate=75.00, license_plate="CST-0001")
        customer = await self._create_customer(client, email="cost@example.com")
        booking_data = {
            "car_id": car["id"],
            "customer_id": customer["id"],
            "start_date": future_date(1),
            "end_date": future_date(6),
        }
        response = await client.post(BOOKINGS_URL, json=booking_data)
        assert response.status_code == 201
        assert response.json()["total_cost"] == 375.00  # 5 days × $75
