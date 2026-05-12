from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.trip import Trip

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    email: str = Field(index=True, unique=True)   
    hashed_password: str
    
    trips: List["Trip"] = Relationship(back_populates="user")