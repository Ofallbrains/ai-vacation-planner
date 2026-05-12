from sqlmodel import Session, select
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripUpdate

def create_trip(session: Session, trip_data: TripCreate, user_id: int):
    trip = Trip(
    destination=trip_data.destination,
    days=trip_data.days,
    budget=trip_data.budget,
    trip_style=trip_data.trip_style,
    user_id=user_id
)
    
    session.add(trip)
    session.commit()
    session.refresh(trip)
    
    return {
    "id": trip.id,
    "destination": trip.destination,
    "days": trip.days,
    "trip_style": trip.trip_style,
    "budget": trip.budget,
    "message": "Trip created successfully"
}
    
def get_user_trips(session: Session, user_id: int):
    return session.exec(
        select(Trip).where(
            Trip.user_id == user_id
        )
    ).all()

def get_trip(session: Session, trip_id: int, user_id: int):
    return session.exec(
        select(Trip).where(
            Trip.id == trip_id,
            Trip.user_id == user_id
        )
    ).first()

    
def update_trip(
    session: Session,
    trip: Trip,
    trip_data: TripUpdate
):

    update_data = trip_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(trip, key, value)

    session.add(trip)
    session.commit()
    session.refresh(trip)

    return trip
    
def delete_trip(session: Session, trip: Trip):
    session.delete(trip)
    session.commit()