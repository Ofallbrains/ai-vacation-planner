from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.dependencies.db import get_session
from app.schemas.itinerary import ItineraryCreate
from app.services.itinerary_service import(create_itinerary, get_itinerary_by_trip, generate_itinerary_for_trip)

router = APIRouter(prefix="/itineraries", tags=["Itineraries"])

def create_new_itinerary(
    data: ItineraryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return create_itinerary(session, data, current_user.id)

@router.get("/{trip_id}")
def get_trip_itinerary(trip_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    
    result = get_itinerary_by_trip(session, trip_id, current_user.id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    return result

@router.post("/generate/{trip_id}")
def generate_ai_itinerary(
    trip_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):

    return generate_itinerary_for_trip(
        session,
        trip_id,
        current_user.id
    )