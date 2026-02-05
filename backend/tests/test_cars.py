"""Tests for Car CRUD operations."""

import pytest
from httpx import AsyncClient


CARS_URL = "/api/v1/cars"

SAMPLE_CAR = {
    "make": "Toyota",
    "model": "Camry",
    "year": 2024,
    "license_plate": "ABC-1234",
    "daily_rate": 49.99,
    "category": "standard",
}


@pytest.mark.asyncio
class TestCreateCar:
    """Tests for POST /api/v1/cars."""

    async def test_create_car(self, client: AsyncClient):
        response = await client.post(CARS_URL, json=SAMPLE_CAR)
        assert response.status_code == 201
        data = response.json()
        assert data["make"] == "Toyota"
        assert data["model"] == "Camry"
        assert data["year"] == 2024
        assert data["license_plate"] == "ABC-1234"
        assert data["daily_rate"] == 49.99
        assert data["category"] == "standard"
        assert data["status"] == "available"
        assert "id" in data
        assert "created_at" in data

    async def test_create_car_duplicate_license_plate(self, client: AsyncClient):
        await client.post(CARS_URL, json=SAMPLE_CAR)
        response = await client.post(CARS_URL, json=SAMPLE_CAR)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    async def test_create_car_missing_required_fields(self, client: AsyncClient):
        response = await client.post(CARS_URL, json={})
        assert response.status_code == 422

    async def test_create_car_invalid_year(self, client: AsyncClient):
        car = {**SAMPLE_CAR, "year": 1800}
        response = await client.post(CARS_URL, json=car)
        assert response.status_code == 422

    async def test_create_car_invalid_daily_rate(self, client: AsyncClient):
        car = {**SAMPLE_CAR, "daily_rate": -10}
        response = await client.post(CARS_URL, json=car)
        assert response.status_code == 422

    async def test_create_car_with_category(self, client: AsyncClient):
        car = {**SAMPLE_CAR, "license_plate": "LUX-001", "category": "luxury"}
        response = await client.post(CARS_URL, json=car)
        assert response.status_code == 201
        assert response.json()["category"] == "luxury"


@pytest.mark.asyncio
class TestListCars:
    """Tests for GET /api/v1/cars."""

    async def test_list_cars_empty(self, client: AsyncClient):
        response = await client.get(CARS_URL)
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_cars(self, client: AsyncClient):
        await client.post(CARS_URL, json=SAMPLE_CAR)
        response = await client.get(CARS_URL)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["license_plate"] == "ABC-1234"

    async def test_list_cars_filter_by_status(self, client: AsyncClient):
        await client.post(CARS_URL, json=SAMPLE_CAR)
        response = await client.get(CARS_URL, params={"status": "available"})
        assert response.status_code == 200
        assert len(response.json()) == 1

        response = await client.get(CARS_URL, params={"status": "rented"})
        assert response.status_code == 200
        assert len(response.json()) == 0

    async def test_list_cars_filter_by_category(self, client: AsyncClient):
        await client.post(CARS_URL, json=SAMPLE_CAR)
        response = await client.get(CARS_URL, params={"category": "standard"})
        assert response.status_code == 200
        assert len(response.json()) == 1

        response = await client.get(CARS_URL, params={"category": "luxury"})
        assert response.status_code == 200
        assert len(response.json()) == 0

    async def test_list_cars_filter_by_status_and_category(self, client: AsyncClient):
        await client.post(CARS_URL, json=SAMPLE_CAR)
        response = await client.get(
            CARS_URL, params={"status": "available", "category": "standard"}
        )
        assert response.status_code == 200
        assert len(response.json()) == 1


@pytest.mark.asyncio
class TestGetCar:
    """Tests for GET /api/v1/cars/{id}."""

    async def test_get_car(self, client: AsyncClient):
        create_resp = await client.post(CARS_URL, json=SAMPLE_CAR)
        car_id = create_resp.json()["id"]

        response = await client.get(f"{CARS_URL}/{car_id}")
        assert response.status_code == 200
        assert response.json()["id"] == car_id
        assert response.json()["make"] == "Toyota"

    async def test_get_car_not_found(self, client: AsyncClient):
        response = await client.get(f"{CARS_URL}/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Car not found"


@pytest.mark.asyncio
class TestUpdateCar:
    """Tests for PUT /api/v1/cars/{id}."""

    async def test_update_car(self, client: AsyncClient):
        create_resp = await client.post(CARS_URL, json=SAMPLE_CAR)
        car_id = create_resp.json()["id"]

        response = await client.put(
            f"{CARS_URL}/{car_id}", json={"daily_rate": 59.99}
        )
        assert response.status_code == 200
        assert response.json()["daily_rate"] == 59.99
        assert response.json()["make"] == "Toyota"  # unchanged fields preserved

    async def test_update_car_status(self, client: AsyncClient):
        create_resp = await client.post(CARS_URL, json=SAMPLE_CAR)
        car_id = create_resp.json()["id"]

        response = await client.put(
            f"{CARS_URL}/{car_id}", json={"status": "maintenance"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "maintenance"

    async def test_update_car_not_found(self, client: AsyncClient):
        response = await client.put(
            f"{CARS_URL}/nonexistent-id", json={"make": "Honda"}
        )
        assert response.status_code == 404

    async def test_update_car_duplicate_license_plate(self, client: AsyncClient):
        await client.post(CARS_URL, json=SAMPLE_CAR)
        car2 = {**SAMPLE_CAR, "license_plate": "XYZ-9999"}
        create_resp = await client.post(CARS_URL, json=car2)
        car2_id = create_resp.json()["id"]

        response = await client.put(
            f"{CARS_URL}/{car2_id}", json={"license_plate": "ABC-1234"}
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
class TestDeleteCar:
    """Tests for DELETE /api/v1/cars/{id}."""

    async def test_delete_car(self, client: AsyncClient):
        create_resp = await client.post(CARS_URL, json=SAMPLE_CAR)
        car_id = create_resp.json()["id"]

        response = await client.delete(f"{CARS_URL}/{car_id}")
        assert response.status_code == 204

        # Verify deleted
        response = await client.get(f"{CARS_URL}/{car_id}")
        assert response.status_code == 404

    async def test_delete_car_not_found(self, client: AsyncClient):
        response = await client.delete(f"{CARS_URL}/nonexistent-id")
        assert response.status_code == 404
