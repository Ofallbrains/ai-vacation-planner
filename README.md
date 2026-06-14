
# AI Vacation Planner API

## Overview

AI Vacation Planner is a backend REST API built with FastAPI and SQLModel that allows users to:

- Register and authenticate accounts
- Create and manage trips
- Create and store travel itineraries
- Generate AI-powered travel itineraries using Anthropic Claude
- Protect user data using JWT authentication

Technologies:
- FastAPI, SQLModel, SQLite, Alembic
- Uvicorn for ASGI hosting
- JWT authentication for route protection
- Anthropic Claude for itinerary generation (LLM)

---

## Features

- JWT-based user registration and login
- CRUD for Trips
- Create, store, and retrieve Itineraries and ItineraryDays
- AI-generated itineraries with structured JSON output
- Ownership checks: users can only access their own trips/itineraries

---

## Project Structure

app/
- dependencies/: FastAPI dependency providers (DB session, auth)
- models/: SQLModel table definitions
- routes/: HTTP endpoints
- schemas/: Pydantic request/response models
- services/: Business logic and adapters (including AI)
- core/: security helpers
- main.py

alembic/: DB migrations

---

**Architecture**

- **Routes Layer**: FastAPI routers receive HTTP requests, perform request validation via schemas, and call service-layer functions. Routes are thin and authorized via dependency-injection (JWT).
- **Service Layer**: Implements business rules, DB transactions, ownership checks, and orchestration (e.g., create trip → optionally call AI itinerary generator). Examples: `trip_service`, `itinerary_service`, `auth_service`, `ai_itinerary_service`.
- **Data Layer / Models**: SQLModel models define tables and relationships (User, Trip, Itinerary, ItineraryDay). The DB is accessed via session objects provided by `dependencies/db.py`.
- **Schemas Layer**: Pydantic models for input validation and output formatting. Schemas are intentionally strict for the AI-produced data to allow robust validation before persisting.
- **Core & Utilities**: `core/security.py` for password hashing & JWT creation; common helpers for retries, caching, and input sanitization.
- **LLM Adapter / AI Service**: A dedicated adapter layer (`services/ai_itinerary_service.py`) encapsulates all LLM interaction, retry/backoff logic, prompt templates, output validation, rate limiting, and optional caching. The rest of the app calls this adapter via a simple function that returns validated itinerary data or a clear error.

Data flow (high-level):
1. Client POSTs trip creation or "generate itinerary" action.
2. Route validates request, confirms user's ownership.
3. Service persists trip (if new) and/or calls AI adapter.
4. AI adapter builds prompt, calls Anthropic, validates structured JSON response, returns it.
5. Service saves itinerary and itinerary_day rows and returns API response.

---

**LLM Integration (Anthropic Claude) — Design & Best Practices**

- **Adapter responsibility**
	- Centralize all LLM calls in `services/ai_itinerary_service.py`.
	- Handle prompt composition, model selection, rate limits, backoff, retries, response parsing, schema validation, and caching.
	- Return clear typed structures (e.g., list of day objects) or raise explicit exceptions the service layer can handle.

- **Environment configuration**
	- `ANTHROPIC_API_KEY` — required API key.
	- `ANTHROPIC_MODEL` — default model overrideable per request.
	- `ANTHROPIC_TIMEOUT` — seconds for HTTP calls.
	- `AI_MAX_TOKENS` / `AI_TEMPERATURE` — tunable inference parameters.

- **Prompting & Template**
	- Use a deterministic prompt template that instructs the model to output only valid JSON following a strict schema.
	- Include explicit constraints: number of days, budget, trip style (budget/standard/luxury), user preferences, travel pace.
	- Example prompt snippet:
		```
		Generate a JSON itinerary for destination "{destination}" for {days} days.
		Output must be a single JSON object matching this schema:
		{
			"trip_id": <int|null>,
			"destination": <string>,
			"days": [
				{ "day": <int>, "activities": [ { "time": <string|null>, "title": <string>, "description": <string>, "cost_estimate": <number|null> } ] }
			],
			"notes": <string|null>
		}
		Respond only with JSON.
		```

- **Output Schema & Validation**
	- Define a strict Pydantic schema for AI output in `schemas/itinerary.py`.
	- Always validate model output before persisting. If validation fails, attempt a structured fallback:
		- Try a single deterministic parse pass.
		- If parsing fails, attempt a small automatic cleanup (strip code fences, trailing text).
		- If still invalid, do not save; return a descriptive error to client and log raw model output for debugging.

- **Retries, Backoff, and Rate Limits**
	- Use exponential backoff with jitter for transient HTTP/429 errors.
	- Cap retries (e.g., 3 attempts).
	- Implement concurrency and rate limiting client-side to avoid hitting provider limits.

- **Caching & Cost Control**
	- Cache common prompts / trip configurations to avoid repeated model calls for identical requests.
	- Consider memoization keyed by (destination, days, trip_style, budget, preferences).
	- Add a `dry_run` or `preview_only` flag to generate itineraries without saving or incurring repeated bets.

- **Safety & Privacy**
	- Do not send user PII (email, exact user id) to LLM provider. Only send trip-relevant, non-identifying fields.
	- Sanitize user-supplied free-text preferences to remove secrets before including them in prompts.
	- Log only metadata and anonymized request info. Never log full prompts containing sensitive user input.

- **Determinism & Reproducibility**
	- For reproducible output (e.g., when users wish to regenerate the same itinerary), set `temperature` low (0–0.3) and store the prompt + model settings used.
	- Save the "model run metadata" with the itinerary: model name, temperature, timestamp, prompt hash.

- **Error handling & UX**
	- If AI generation fails, the API should:
		- Return a clear 502/503 response with an explanation like "AI generation failed. Please try again."
		- Optionally fall back to a simple rule-based generator for minimal output.
	- Expose generation status (pending/complete/failed) for long-running operations; use background tasks for large models.

---

## Database Design

- **User**: id, email, hashed_password
- **Trip**: id, destination, days, budget, trip_style, user_id
- **Itinerary**: id, trip_id, generated_by_ai (bool), model_metadata (json optional)
- **ItineraryDay**: id, day, activities (JSON), itinerary_id

---

## Setup Instructions

1. Create and activate virtual environment (Windows example):
	 ```
	 py -m venv venv
	 .\venv\Scripts\Activate.ps1
	 ```
2. Install requirements:
	 ```
	 pip install -r requirements.txt
	 ```
3. Configure environment variables:
	 - `DATABASE_URL` (e.g., sqlite:///./dev.db)
	 - `SECRET_KEY` (JWT secret)
	 - `ANTHROPIC_API_KEY`
	 - Optional: `ANTHROPIC_MODEL`, `ANTHROPIC_TIMEOUT`, `AI_TEMPERATURE`
4. Run migrations:
	 ```
	 alembic upgrade head
	 ```
5. Start server:
	 ```
	 uvicorn app.main:app --reload
	 ```

---

## API Documentation

Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## Example Endpoints

- `POST /auth/register` — Register
- `POST /auth/login` — Login
- `GET /users/me` — Protected
- `POST /trips` — Create trip
- `POST /itineraries/generate` — Generate itinerary using AI (protected)
- `GET /itineraries/{trip_id}` — Retrieve itinerary

---
