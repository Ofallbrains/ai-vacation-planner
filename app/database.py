from sqlmodel import create_engine, SQLModel
from app.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug
)