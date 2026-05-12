from pydantic import BaseModel
from typing import Optional

class TripCreate(BaseModel):
    destination: str
    days: int
    budget: float
    trip_style: str

class TripResponse(BaseModel):
    id: int
    destination: str
    days: int
    budget: float
    trip_style: str
    message: str
    
class TripRead(BaseModel):
    id: int
    destination: str
    days: int
    budget: float
    trip_style: str
    
class TripUpdate(BaseModel):
    destination: Optional[str] = None
    days: Optional[int] = None
    budget: Optional[float] = None
    trip_style: Optional[str] = None