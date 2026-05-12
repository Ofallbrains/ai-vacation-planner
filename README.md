
# AI Vacation Planner API

## Overview

AI Vacation Planner is a backend REST API built with FastAPI and SQLModel that allows users to:

- Register and authenticate accounts
- Create and manage trips
- Create and store travel itineraries
- Protect user data using JWT authentication

The project follows a clean backend structure using:

- FastAPI
- SQLModel
- SQLite
- Alembic
- JWT Authentication

---

## Features

### Authentication

- Register user
- Login user
- JWT token authentication
- Protected routes

### Trips

- Create trip
- Get all trips
- Get single trip
- Update trip
- Delete trip

### Itineraries

- Create itinerary
- Store itinerary days and activities
- Get itinerary by trip
- User ownership protection

---

## Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite
- Alembic
- JWT Authentication
- Uvicorn

---

## Project Structure

```bash
app/
│
├── dependencies/
│   ├── auth.py
│   └── db.py
│
├── models/
│   ├── user.py
│   ├── trip.py
│   ├── itinerary.py
│   └── itinerary_day.py
│
├── routes/
│   ├── auth.py
│   ├── user.py
│   ├── trips.py
│   └── itinerary.py
│
├── schemas/
│   ├── auth.py
│   ├── trip.py
│   └── itinerary.py
│
├── services/
│   ├── auth_service.py
│   ├── trip_service.py
│   └── itinerary_service.py
│
├── core/
│   └── security.py
│
└── main.py

alembic/
requirements.txt
README.md
```

---

## Architecture Explanation

The project uses a layered backend architecture.

### Routes Layer

Handles API endpoints and HTTP requests.

Example:

```python
@router.post("/")
def create_new_trip():
		...
```

Responsibilities:

- Receive requests
- Validate request data
- Call services
- Return responses

---

### Service Layer

Contains business logic.

Example:

```python
def create_trip(session, trip_data, user_id):
		...
```

Responsibilities:

- Database operations
- Authorization checks
- Business rules
- CRUD logic

---

### Models Layer

Defines database tables using SQLModel.

Example:

```python
class Trip(SQLModel, table=True):
		...
```

Responsibilities:

- Database schema
- Relationships
- Table structure

---

### Schemas Layer

Defines request and response validation using Pydantic.

Example:

```python
class TripCreate(BaseModel):
		...
```

Responsibilities:

- Input validation
- Response formatting
- API contracts

---

## Database Design

### User

Stores user authentication information.

Fields:

- id
- email
- hashed_password

---

### Trip

Stores trip information.

Fields:

- id
- destination
- days
- budget
- trip_style
- user_id

Relationship:

- A trip belongs to one user.

---

### Itinerary

Stores itinerary information linked to a trip.

Fields:

- id
- trip_id

Relationship:

- An itinerary belongs to one trip.

---

### ItineraryDay

Stores activities for each itinerary day.

Fields:

- id
- day
- activities
- itinerary_id

Relationship:

- Multiple itinerary days belong to one itinerary.

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd ai-vacation-planner
```

---

### 2. Create Virtual Environment

#### Windows

```bash
py -m venv venv
.\venv\Scripts\Activate.ps1
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run Database Migrations

```bash
alembic upgrade head
```

---

### 5. Start Server

```bash
uvicorn app.main:app --reload
```

Server URL:

```bash
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates Swagger documentation.

### Swagger UI

Open:

```bash
http://127.0.0.1:8000/docs
```

---

## API Endpoints

## Authentication

### Register User

```http
POST /auth/register
```

Request:

```json
{
	"email": "user1@test.com",
	"password": "12345678"
}
```

---

### Login User

```http
POST /auth/login
```

Request:

```json
{
	"email": "user1@test.com",
	"password": "12345678"
}
```

---

### Get Current User

```http
GET /users/me
```

Protected Route:

```text
Authorization: Bearer <token>
```

---

## Trips

### Create Trip

```http
POST /trips
```

Request:

```json
{
	"destination": "Paris",
	"days": 5,
	"budget": 1500,
	"trip_style": "budget"
}
```

Response:

```json
{
	"id": 1,
	"destination": "Paris",
	"days": 5,
	"budget": 1500,
	"trip_style": "budget",
	"message": "Trip created successfully"
}
```

---

### Get All Trips

```http
GET /trips
```

---

### Get Single Trip

```http
GET /trips/{id}
```

---

### Update Trip

```http
PUT /trips/{id}
```

---

### Delete Trip

```http
DELETE /trips/{id}
```

---

## Itineraries

### Create Itinerary

```http
POST /itineraries
```

Request:

```json
{
	"trip_id": 1,
	"days": [
		{
			"day": 1,
			"activities": ["Eiffel Tower", "Seine River Walk"]
		},
		{
			"day": 2,
			"activities": ["Louvre Museum", "Montmartre"]
		}
	]
}
```

Response:

```json
{
	"trip_id": 1,
	"itinerary": [
		{
			"day": 1,
			"activities": ["Eiffel Tower", "Seine River Walk"]
		},
		{
			"day": 2,
			"activities": ["Louvre Museum", "Montmartre"]
		}
	],
	"message": "Itinerary created successfully"
}
```

---

### Get Itinerary By Trip

```http
GET /itineraries/{trip_id}
```

---

## Authentication Flow

1. Register user
2. Login user
3. Copy JWT token
4. Click "Authorize" in Swagger
5. Enter:

```text
your_token_here
```

6. Access protected routes

---

## Security

The application uses JWT authentication for route protection.

Protected resources:

- User profile
- Trips
- Itineraries

Users can only access their own trips and itineraries.

---
