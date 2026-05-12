import json
from sqlmodel import Session
from fastapi import HTTPException

from app.models.trip import Trip
from app.models.itinerary import Itinerary
from app.models.itinerary_day import ItineraryDay
from app.schemas.itinerary import ItineraryCreate

def create_itinerary(session: Session, data: ItineraryCreate, user_id: int):
    
    trip = session.get(Trip, data.trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    itinerary = Itinerary(trip_id=data.trip_id)
    session.add(itinerary)
    session.flush()  # IMPORTANT: get itinerary.id without commit

    for d in data.days:
        day = ItineraryDay(
            day=d.day,
            activities=json.dumps(d.activities),
            itinerary_id=itinerary.id
        )
        session.add(day)

    session.commit()

    return {
        "trip_id": data.trip_id,
        "itinerary": data.days,
        "message": "Itinerary created successfully"
    }

def get_itinerary_by_trip(session: Session, trip_id: int, user_id: int):
    
    trip = session.get(Trip, trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    itinerary = session.query(Itinerary).filter(
        Itinerary.trip_id == trip_id
    ).first()

    if not itinerary:
        return None

    days = session.query(ItineraryDay).filter(
        ItineraryDay.itinerary_id == itinerary.id
    ).all()

    return {
        "trip_id": trip_id,
        "itinerary": [
            {
                "day": d.day,
                "activities": json.loads(d.activities)
            }
            for d in days
        ]
    }