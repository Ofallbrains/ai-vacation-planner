from pydantic import BaseModel
from typing import List

class DayCreate(BaseModel):
    day: int
    activities: List[str]
    
class ItineraryCreate(BaseModel):
    trip_id: int
    days: List[DayCreate]