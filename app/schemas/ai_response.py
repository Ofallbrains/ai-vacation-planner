from pydantic import BaseModel

class DaySchema(BaseModel):
    day: int
    activities: list[str]


class AIItineraryResponse(BaseModel):
    days: list[DaySchema]