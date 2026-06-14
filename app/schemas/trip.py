from pydantic import BaseModel, Field
from typing import Optional

class TripCreate(BaseModel):
    destination: str = Field(min_length=1)
    days: int = Field(ge=1)
    budget: float = Field(ge=0)
    trip_style: str = Field(min_length=1)

class TripUpdate(BaseModel):
    destination: Optional[str] = Field(default=None, min_length=1)
    days: Optional[int] = Field(default=None, ge=1)
    budget: Optional[float] = Field(default=None, ge=0)
    trip_style: Optional[str] = Field(default=None, min_length=1)

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
    