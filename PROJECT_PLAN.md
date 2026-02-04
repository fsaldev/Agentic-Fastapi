# Rent a Car Backend API - Project Plan

## Overview

A RESTful backend API for managing a car rental business. Handles car inventory, customer records, and the full booking lifecycle (reservation → rental → return). Built with FastAPI for modern async support and SQLite for simplicity.

## Technical Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite with async SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **Architecture**: Layered (Routes → Services → Repositories)

---

## Data Models

### Car

| Field         | Type     | Notes            |
|---------------|----------|------------------|
| id            | UUID     | Primary key      |
| make          | string   | e.g., "Toyota"   |
| model         | string   | e.g., "Camry"    |
| year          | int      | e.g., 2023       |
| license_plate | string   | Unique           |
| daily_rate    | decimal  | Price per day    |
| category      | enum     | economy, standard, luxury, suv |
| status        | enum     | available, rented, maintenance |
| created_at    | datetime |                  |

### Customer

| Field          | Type     | Notes       |
|----------------|----------|-------------|
| id             | UUID     | Primary key |
| first_name     | string   |             |
| last_name      | string   |             |
| email          | string   | Unique      |
| phone          | string   |             |
| driver_license | string   |             |
| created_at     | datetime |             |

### Booking

| Field              | Type     | Notes             |
|--------------------|----------|-------------------|
| id                 | UUID     | Primary key       |
| car_id             | UUID     | FK → Car          |
| customer_id        | UUID     | FK → Customer     |
| start_date         | date     | Pickup date       |
| end_date           | date     | Expected return   |
| actual_return_date | date     | Nullable          |
| total_cost         | decimal  | Calculated        |
| status             | enum     | reserved, active, completed, cancelled |
| created_at         | datetime |                   |

---

## API Endpoints

### Cars `/api/v1/cars`

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| GET    | `/`               | List all cars (filter by status, category) |
| GET    | `/{id}`           | Get car details                    |
| POST   | `/`               | Add new car                        |
| PUT    | `/{id}`           | Update car                         |
| DELETE | `/{id}`           | Delete car                         |
| GET    | `/{id}/availability` | Check availability for date range |

### Customers `/api/v1/customers`

| Method | Endpoint  | Description         |
|--------|-----------|---------------------|
| GET    | `/`       | List customers      |
| GET    | `/{id}`   | Get customer details|
| POST   | `/`       | Register customer   |
| PUT    | `/{id}`   | Update customer     |
| DELETE | `/{id}`   | Delete customer     |

### Bookings `/api/v1/bookings`

| Method | Endpoint        | Description                          |
|--------|-----------------|--------------------------------------|
| GET    | `/`             | List bookings (filter by status, customer, car) |
| GET    | `/{id}`         | Get booking details                  |
| POST   | `/`             | Create booking (reserve)             |
| POST   | `/{id}/pickup`  | Start rental (reserved → active)     |
| POST   | `/{id}/return`  | Return car (active → completed)      |
| POST   | `/{id}/cancel`  | Cancel booking                       |

---

## Folder Structure

```
app/
├── main.py                 # FastAPI app entry point
├── config.py               # Settings & configuration
├── database.py             # DB connection & session
│
├── models/                 # SQLAlchemy models
│   ├── __init__.py
│   ├── car.py
│   ├── customer.py
│   └── booking.py
│
├── schemas/                # Pydantic schemas
│   ├── __init__.py
│   ├── car.py
│   ├── customer.py
│   └── booking.py
│
├── repositories/           # Data access layer
│   ├── __init__.py
│   ├── base.py
│   ├── car.py
│   ├── customer.py
│   └── booking.py
│
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── car.py
│   ├── customer.py
│   └── booking.py
│
├── api/                    # API routes
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── router.py       # Aggregates all v1 routes
│   │   ├── cars.py
│   │   ├── customers.py
│   │   └── bookings.py
│   └── dependencies.py     # Shared dependencies
│
└── exceptions/             # Custom exceptions
    ├── __init__.py
    └── handlers.py
```

---

## Features

### MVP Features

| #   | Feature                    | Priority | Dependencies |
|-----|----------------------------|----------|--------------|
| 1   | Project setup & database   | P1       | None         |
| 2   | Car CRUD operations        | P1       | 1            |
| 3   | Customer CRUD operations   | P1       | 1            |
| 4   | Create booking (reservation) | P1     | 2, 3         |
| 5   | Car availability check     | P1       | 2, 4         |
| 6   | Pickup car (start rental)  | P1       | 4            |
| 7   | Return car (complete rental) | P1     | 6            |

### Dependency Graph

```
[1] Project Setup
 ├── [2] Car CRUD
 │    └── [5] Availability Check
 └── [3] Customer CRUD
      └── [4] Create Booking
           └── [6] Pickup Car
                └── [7] Return Car
```

---

## Feature Details

### 1. Project Setup & Database

**Description**: Initialize the FastAPI project with the layered architecture, configure async SQLAlchemy with SQLite, and create all database models.

**Acceptance Criteria**:
- [ ] FastAPI application starts successfully
- [ ] Database tables are created on startup
- [ ] Project follows the defined folder structure
- [ ] Configuration management is in place

---

### 2. Car CRUD Operations

**Description**: Implement full Create, Read, Update, Delete operations for cars with filtering capabilities.

**Acceptance Criteria**:
- [ ] POST `/api/v1/cars` - Create a new car
- [ ] GET `/api/v1/cars` - List all cars with optional filters (status, category)
- [ ] GET `/api/v1/cars/{id}` - Get car by ID
- [ ] PUT `/api/v1/cars/{id}` - Update car details
- [ ] DELETE `/api/v1/cars/{id}` - Delete a car
- [ ] Validation: License plate must be unique
- [ ] Proper error responses (404, 400, etc.)

---

### 3. Customer CRUD Operations

**Description**: Implement full Create, Read, Update, Delete operations for customers.

**Acceptance Criteria**:
- [ ] POST `/api/v1/customers` - Register a new customer
- [ ] GET `/api/v1/customers` - List all customers
- [ ] GET `/api/v1/customers/{id}` - Get customer by ID
- [ ] PUT `/api/v1/customers/{id}` - Update customer details
- [ ] DELETE `/api/v1/customers/{id}` - Delete a customer
- [ ] Validation: Email must be unique
- [ ] Proper error responses (404, 400, etc.)

---

### 4. Create Booking (Reservation)

**Description**: Allow customers to create a booking/reservation for a car within a specified date range.

**Acceptance Criteria**:
- [ ] POST `/api/v1/bookings` - Create a new booking
- [ ] Validate car exists and is not in maintenance
- [ ] Validate customer exists
- [ ] Validate date range (start_date < end_date, start_date >= today)
- [ ] Check car availability for the requested dates
- [ ] Calculate total_cost = daily_rate × number of days
- [ ] Set booking status to "reserved"
- [ ] Prevent double-booking (same car, overlapping dates)

---

### 5. Car Availability Check

**Description**: Check if a specific car is available for a given date range.

**Acceptance Criteria**:
- [ ] GET `/api/v1/cars/{id}/availability?start_date=X&end_date=Y`
- [ ] Returns availability status (true/false)
- [ ] If unavailable, returns conflicting booking dates
- [ ] Considers bookings with status "reserved" or "active"
- [ ] Does not consider "completed" or "cancelled" bookings

---

### 6. Pickup Car (Start Rental)

**Description**: Transition a booking from reserved to active when the customer picks up the car.

**Acceptance Criteria**:
- [ ] POST `/api/v1/bookings/{id}/pickup`
- [ ] Validate booking exists and status is "reserved"
- [ ] Update booking status to "active"
- [ ] Update car status to "rented"
- [ ] Return updated booking details

---

### 7. Return Car (Complete Rental)

**Description**: Complete a rental when the customer returns the car.

**Acceptance Criteria**:
- [ ] POST `/api/v1/bookings/{id}/return`
- [ ] Validate booking exists and status is "active"
- [ ] Set actual_return_date to current date
- [ ] Update booking status to "completed"
- [ ] Update car status to "available"
- [ ] Return updated booking details with final cost

---

## Future Enhancements (Phase 2)

- Search/filter cars by multiple criteria
- Booking history and reports
- Late fee calculation
- Customer booking history endpoint
- Pagination for list endpoints
- Authentication and authorization
