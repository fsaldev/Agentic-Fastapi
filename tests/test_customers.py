"""Tests for Customer CRUD operations."""

import pytest
from httpx import AsyncClient


CUSTOMERS_URL = "/api/v1/customers"

SAMPLE_CUSTOMER = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "driver_license": "DL-123456",
}


@pytest.mark.asyncio
class TestCreateCustomer:
    """Tests for POST /api/v1/customers."""

    async def test_create_customer(self, client: AsyncClient):
        response = await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["email"] == "john.doe@example.com"
        assert data["phone"] == "+1234567890"
        assert data["driver_license"] == "DL-123456"
        assert "id" in data
        assert "created_at" in data

    async def test_create_customer_duplicate_email(self, client: AsyncClient):
        await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        response = await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    async def test_create_customer_missing_required_fields(self, client: AsyncClient):
        response = await client.post(CUSTOMERS_URL, json={})
        assert response.status_code == 422

    async def test_create_customer_invalid_email(self, client: AsyncClient):
        customer = {**SAMPLE_CUSTOMER, "email": "not-an-email"}
        response = await client.post(CUSTOMERS_URL, json=customer)
        assert response.status_code == 422


@pytest.mark.asyncio
class TestListCustomers:
    """Tests for GET /api/v1/customers."""

    async def test_list_customers_empty(self, client: AsyncClient):
        response = await client.get(CUSTOMERS_URL)
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_customers(self, client: AsyncClient):
        await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        response = await client.get(CUSTOMERS_URL)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["email"] == "john.doe@example.com"

    async def test_list_multiple_customers(self, client: AsyncClient):
        await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        customer2 = {**SAMPLE_CUSTOMER, "email": "jane.doe@example.com", "first_name": "Jane"}
        await client.post(CUSTOMERS_URL, json=customer2)
        response = await client.get(CUSTOMERS_URL)
        assert response.status_code == 200
        assert len(response.json()) == 2


@pytest.mark.asyncio
class TestGetCustomer:
    """Tests for GET /api/v1/customers/{id}."""

    async def test_get_customer(self, client: AsyncClient):
        create_resp = await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        customer_id = create_resp.json()["id"]

        response = await client.get(f"{CUSTOMERS_URL}/{customer_id}")
        assert response.status_code == 200
        assert response.json()["id"] == customer_id
        assert response.json()["first_name"] == "John"

    async def test_get_customer_not_found(self, client: AsyncClient):
        response = await client.get(f"{CUSTOMERS_URL}/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"


@pytest.mark.asyncio
class TestUpdateCustomer:
    """Tests for PUT /api/v1/customers/{id}."""

    async def test_update_customer(self, client: AsyncClient):
        create_resp = await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        customer_id = create_resp.json()["id"]

        response = await client.put(
            f"{CUSTOMERS_URL}/{customer_id}", json={"first_name": "Jonathan"}
        )
        assert response.status_code == 200
        assert response.json()["first_name"] == "Jonathan"
        assert response.json()["last_name"] == "Doe"  # unchanged fields preserved

    async def test_update_customer_email(self, client: AsyncClient):
        create_resp = await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        customer_id = create_resp.json()["id"]

        response = await client.put(
            f"{CUSTOMERS_URL}/{customer_id}", json={"email": "new.email@example.com"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == "new.email@example.com"

    async def test_update_customer_not_found(self, client: AsyncClient):
        response = await client.put(
            f"{CUSTOMERS_URL}/nonexistent-id", json={"first_name": "Jane"}
        )
        assert response.status_code == 404

    async def test_update_customer_duplicate_email(self, client: AsyncClient):
        await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        customer2 = {**SAMPLE_CUSTOMER, "email": "jane.doe@example.com"}
        create_resp = await client.post(CUSTOMERS_URL, json=customer2)
        customer2_id = create_resp.json()["id"]

        response = await client.put(
            f"{CUSTOMERS_URL}/{customer2_id}", json={"email": "john.doe@example.com"}
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
class TestDeleteCustomer:
    """Tests for DELETE /api/v1/customers/{id}."""

    async def test_delete_customer(self, client: AsyncClient):
        create_resp = await client.post(CUSTOMERS_URL, json=SAMPLE_CUSTOMER)
        customer_id = create_resp.json()["id"]

        response = await client.delete(f"{CUSTOMERS_URL}/{customer_id}")
        assert response.status_code == 204

        # Verify deleted
        response = await client.get(f"{CUSTOMERS_URL}/{customer_id}")
        assert response.status_code == 404

    async def test_delete_customer_not_found(self, client: AsyncClient):
        response = await client.delete(f"{CUSTOMERS_URL}/nonexistent-id")
        assert response.status_code == 404
