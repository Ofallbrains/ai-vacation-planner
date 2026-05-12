from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User


class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    destination: str
    days: int
    budget: float
    trip_style: str
    
    user_id: int = Field(foreign_key="user.id")
    
    user: Optional["User"] = Relationship(back_populates="trips")