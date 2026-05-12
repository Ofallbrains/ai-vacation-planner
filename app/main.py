from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.trips import router as trips_router
from app.routes.itinerary import router as itinerary_router


import app.models

app = FastAPI(title="AI Vacation Planner")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"message": "API running"}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(trips_router)
app.include_router(itinerary_router)