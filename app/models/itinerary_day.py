from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.itinerary import Itinerary

class ItineraryDay(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    day: int
    activities: str
    itinerary_id: int = Field(foreign_key="itinerary.id")
    itinerary: Optional["Itinerary"] = Relationship(back_populates="days")