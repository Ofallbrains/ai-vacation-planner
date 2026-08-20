from pydantic import BaseModel


class DayCreate(BaseModel):
    day: int
    activities: list[str]


class ItineraryCreate(BaseModel):
    trip_id: int
    days: list[DayCreate]


class ItineraryResponse(BaseModel):
    trip_id: int
    itinerary: list[DayCreate]
    message: str