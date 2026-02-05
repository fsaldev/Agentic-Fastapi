# Rent a Car API

A RESTful backend API for managing a car rental business built with FastAPI, SQLAlchemy, and SQLite.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)
  - [Health Check](#health-check)
  - [Cars API](#cars-api)
  - [Customers API](#customers-api)
  - [Bookings API](#bookings-api)
- [Data Models](#data-models)
  - [Car](#car)
  - [Customer](#customer)
  - [Booking](#booking)
- [Testing](#testing)
  - [Running Tests](#running-tests)
  - [Test Coverage](#test-coverage)
- [Configuration](#configuration)
- [Architecture](#architecture)

## Overview

This API provides complete functionality for managing a car rental business including:

- **Car Management**: Add, update, delete, and list vehicles in the fleet
- **Customer Management**: Register and manage customer information
- **Booking Management**: Create reservations, track rental lifecycle (pickup, return, cancel)
- **Availability Checking**: Check car availability for specific date ranges

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | >= 3.11 | Runtime |
| FastAPI | >= 0.109.0 | Web Framework |
| SQLAlchemy | >= 2.0.0 | ORM |
| aiosqlite | >= 0.19.0 | Async SQLite Driver |
| Pydantic | >= 2.0.0 | Data Validation |
| Uvicorn | >= 0.27.0 | ASGI Server |
| pytest | >= 8.0.0 | Testing |
| httpx | >= 0.26.0 | HTTP Client for Tests |

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Application settings
│   ├── database.py             # Database connection setup
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # Dependency injection
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # API router aggregation
│   │       ├── cars.py         # Car endpoints
│   │       ├── customers.py    # Customer endpoints
│   │       └── bookings.py     # Booking endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # SQLAlchemy base model
│   │   ├── car.py              # Car model
│   │   ├── customer.py         # Customer model
│   │   └── booking.py          # Booking model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── car.py              # Car Pydantic schemas
│   │   ├── customer.py         # Customer Pydantic schemas
│   │   └── booking.py          # Booking Pydantic schemas
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py             # Base repository pattern
│   │   ├── car.py              # Car repository
│   │   ├── customer.py         # Customer repository
│   │   └── booking.py          # Booking repository
│   ├── services/
│   │   ├── __init__.py
│   │   ├── car.py              # Car business logic
│   │   ├── customer.py         # Customer business logic
│   │   └── booking.py          # Booking business logic
│   └── exceptions/
│       ├── __init__.py
│       └── handlers.py         # Exception handlers
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Test fixtures
│   ├── test_cars.py            # Car API tests
│   ├── test_customers.py       # Customer API tests
│   └── test_bookings.py        # Booking API tests
├── pyproject.toml              # Project dependencies
└── uv.lock                     # Lock file
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agentic-ai-project
   ```

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Install dependencies using uv**
   ```bash
   uv sync
   ```

   Or with pip:
   ```bash
   pip install -e .
   ```

4. **Install development dependencies** (for testing)
   ```bash
   uv sync --extra dev
   ```

   Or with pip:
   ```bash
   pip install -e ".[dev]"
   ```

### Running the Server

Start the development server:

```bash
cd backend
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Documentation

Base URL: `/api/v1`

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API health status |

**Response:**
```json
{
  "status": "healthy"
}
```

### Cars API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cars` | List all cars |
| GET | `/api/v1/cars/{car_id}` | Get car by ID |
| POST | `/api/v1/cars` | Create a new car |
| PUT | `/api/v1/cars/{car_id}` | Update a car |
| DELETE | `/api/v1/cars/{car_id}` | Delete a car |
| GET | `/api/v1/cars/{car_id}/availability` | Check car availability |

#### Query Parameters for List Cars

| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by status: `available`, `rented`, `maintenance` |
| category | string | Filter by category: `economy`, `standard`, `luxury`, `suv` |

#### Create Car Request Body

```json
{
  "make": "Toyota",
  "model": "Camry",
  "year": 2023,
  "license_plate": "ABC-1234",
  "daily_rate": 50.00,
  "category": "standard"
}
```

#### Car Response

```json
{
  "id": "uuid-string",
  "make": "Toyota",
  "model": "Camry",
  "year": 2023,
  "license_plate": "ABC-1234",
  "daily_rate": 50.00,
  "category": "standard",
  "status": "available",
  "created_at": "2024-01-01T00:00:00"
}
```

### Customers API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/customers` | List all customers |
| GET | `/api/v1/customers/{customer_id}` | Get customer by ID |
| POST | `/api/v1/customers` | Create a new customer |
| PUT | `/api/v1/customers/{customer_id}` | Update a customer |
| DELETE | `/api/v1/customers/{customer_id}` | Delete a customer |

#### Create Customer Request Body

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "driver_license": "DL123456"
}
```

#### Customer Response

```json
{
  "id": "uuid-string",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "driver_license": "DL123456",
  "created_at": "2024-01-01T00:00:00"
}
```

### Bookings API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/bookings` | List all bookings |
| GET | `/api/v1/bookings/{booking_id}` | Get booking by ID |
| POST | `/api/v1/bookings` | Create a new booking |
| POST | `/api/v1/bookings/{booking_id}/pickup` | Start rental (reserved -> active) |
| POST | `/api/v1/bookings/{booking_id}/return` | Complete rental (active -> completed) |
| POST | `/api/v1/bookings/{booking_id}/cancel` | Cancel a booking |

#### Query Parameters for List Bookings

| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by status: `reserved`, `active`, `completed`, `cancelled` |
| car_id | string | Filter by car ID |
| customer_id | string | Filter by customer ID |

#### Create Booking Request Body

```json
{
  "car_id": "car-uuid",
  "customer_id": "customer-uuid",
  "start_date": "2024-01-15",
  "end_date": "2024-01-20"
}
```

#### Booking Response

```json
{
  "id": "uuid-string",
  "car_id": "car-uuid",
  "customer_id": "customer-uuid",
  "start_date": "2024-01-15",
  "end_date": "2024-01-20",
  "actual_return_date": null,
  "total_cost": 250.00,
  "status": "reserved",
  "created_at": "2024-01-01T00:00:00"
}
```

#### Booking Lifecycle

```
    ┌──────────┐
    │ RESERVED │ ──────────────────────────┐
    └────┬─────┘                           │
         │ POST /pickup                    │ POST /cancel
         ▼                                 ▼
    ┌──────────┐                     ┌───────────┐
    │  ACTIVE  │                     │ CANCELLED │
    └────┬─────┘                     └───────────┘
         │ POST /return
         ▼
    ┌───────────┐
    │ COMPLETED │
    └───────────┘
```

## Data Models

### Car

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| make | string | Car manufacturer (max 100 chars) |
| model | string | Car model name (max 100 chars) |
| year | integer | Manufacturing year (1900-2100) |
| license_plate | string | Unique license plate (max 20 chars) |
| daily_rate | decimal | Rental price per day (> 0) |
| category | enum | `economy`, `standard`, `luxury`, `suv` |
| status | enum | `available`, `rented`, `maintenance` |
| created_at | datetime | Record creation timestamp |

### Customer

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| first_name | string | Customer first name (max 100 chars) |
| last_name | string | Customer last name (max 100 chars) |
| email | string | Unique email address |
| phone | string | Phone number (max 20 chars) |
| driver_license | string | Driver license number (max 50 chars) |
| created_at | datetime | Record creation timestamp |

### Booking

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| car_id | UUID | Reference to car |
| customer_id | UUID | Reference to customer |
| start_date | date | Rental start date |
| end_date | date | Expected return date |
| actual_return_date | date | Actual return date (nullable) |
| total_cost | decimal | Total rental cost |
| status | enum | `reserved`, `active`, `completed`, `cancelled` |
| created_at | datetime | Record creation timestamp |

## Testing

### Running Tests

Run all tests from the backend directory:

```bash
cd backend
uv run pytest
```

Run tests with verbose output:

```bash
uv run pytest -v
```

Run specific test file:

```bash
uv run pytest tests/test_cars.py -v
uv run pytest tests/test_customers.py -v
uv run pytest tests/test_bookings.py -v
```

Run specific test class:

```bash
uv run pytest tests/test_cars.py::TestCreateCar -v
```

Run specific test:

```bash
uv run pytest tests/test_cars.py::TestCreateCar::test_create_car -v
```

### Test Coverage

The test suite includes **53 tests** covering:

#### Car Tests (18 tests)

| Test Class | Tests | Description |
|------------|-------|-------------|
| TestCreateCar | 6 | Create car, duplicate license plate, missing fields, invalid year/rate, with category |
| TestListCars | 5 | Empty list, list cars, filter by status, filter by category, combined filters |
| TestGetCar | 2 | Get existing car, car not found |
| TestUpdateCar | 4 | Update car, update status, not found, duplicate license plate |
| TestDeleteCar | 2 | Delete car, not found |

#### Customer Tests (15 tests)

| Test Class | Tests | Description |
|------------|-------|-------------|
| TestCreateCustomer | 4 | Create customer, duplicate email, missing fields, invalid email |
| TestListCustomers | 3 | Empty list, list customers, multiple customers |
| TestGetCustomer | 2 | Get existing customer, not found |
| TestUpdateCustomer | 4 | Update customer, update email, not found, duplicate email |
| TestDeleteCustomer | 2 | Delete customer, not found |

#### Booking Tests (20 tests)

| Test Class | Tests | Description |
|------------|-------|-------------|
| TestCreateBooking | 9 | Create booking, car not found, car in maintenance, customer not found, date validations, double booking prevention, cost calculation |
| TestCarAvailability | 4 | Car available, unavailable with conflicts, completed/cancelled bookings ignored |
| TestPickupCar | 3 | Pickup success, booking not found, wrong status |
| TestReturnCar | 3 | Return success, booking not found, wrong status |

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the backend directory:

```env
APP_NAME=Rent a Car API
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:///./rent_a_car.db
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| APP_NAME | "Rent a Car API" | Application name |
| DEBUG | false | Enable debug mode |
| DATABASE_URL | sqlite+aiosqlite:///./rent_a_car.db | Database connection string |

## Architecture

The application follows a layered architecture pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                             │
│  (FastAPI routers - handles HTTP requests/responses)         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Service Layer                            │
│  (Business logic, validation, orchestration)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Repository Layer                           │
│  (Data access, database operations)                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Database                                 │
│  (SQLite with SQLAlchemy ORM)                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Patterns

- **Repository Pattern**: Abstracts database operations
- **Dependency Injection**: FastAPI's `Depends()` for loose coupling
- **Pydantic Schemas**: Request/response validation and serialization
- **Async/Await**: Non-blocking I/O for better performance

## License

This project is proprietary and confidential.
