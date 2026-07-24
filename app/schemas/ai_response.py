from pydantic import BaseModel, Field

class DaySchema(BaseModel):
    day: int
    activities: list[str]


class AIItineraryResponse(BaseModel):
    days: list[DaySchema]