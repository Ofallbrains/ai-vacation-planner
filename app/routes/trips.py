from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.dependencies.db import get_session
from app.dependencies.auth import get_current_user

from app.models.user import User
from app.schemas.trip import TripCreate, TripUpdate
from app.services.trip_service import(
    create_trip,
    get_user_trips,
    get_trip,
    update_trip,
    delete_trip
)

router = APIRouter(prefix="/trips", tags=["Trips"])

# create trip

@router.post("/")
def create_new_trip(
    trip_data: TripCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    return create_trip(
        session,
        trip_data,
        current_user.id
    )
    
# get all trips

@router.get("/")
def get_trips(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    return get_user_trips(
        session,
        current_user.id,
        
    )
    
# get single trip

@router.get("/{trip_id}")
def get_single_trip(
    trip_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    trip = get_trip(session, trip_id, current_user.id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return trip

# update trip
@router.put("/{trip_id}")
def update_user_trip(
    trip_id: int,
    trip_data: TripUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    trip = get_trip(session, trip_id, current_user.id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found"
        )

    updated_trip = update_trip(session, trip, trip_data
    )

    return updated_trip

# delete trip

@router.delete("/{trip_id}")
def delete_user_trip(
    trip_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    trip = get_trip(session, trip_id, current_user.id)
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    delete_trip(session, trip)
    
    return {"message": "Trip deleted successfully"}
    