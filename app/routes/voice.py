import os
import tempfile

from fastapi import Depends
from fastapi.responses import FileResponse
from sqlmodel import Session

from app.dependencies.db import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.itinerary_service import get_itinerary_by_trip
from app.services.tts_service import text_to_speech

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.agents.travel_agent import run_agent
from app.schemas.ai_response import AIItineraryResponse
from app.services.speech_service import transcribe_audio


router = APIRouter(
    prefix="/voice",
    tags=["Voice"],
)

@router.post(
    "/plan",
    response_model=AIItineraryResponse,
)
async def plan_from_voice(
    audio: UploadFile = File(...),
):
    allowed_audio_types = (
        "audio/wav",
        "audio/mpeg",
        "audio/mp4",
        "audio/mp3",
        "audio/x-m4a",
        "audio/webm",
        "video/mp4",
    )

    if audio.content_type not in allowed_audio_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format",
        )

    temp_path = None

    try:
        
        suffix = os.path.splitext(
            audio.filename or ""
        )[1] or ".wav"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                await audio.read()
            )

            temp_path = temp_file.name

        transcript = transcribe_audio(temp_path)

        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="Could not understand the audio",
            )

        print("Transcript:", transcript)

        result = run_agent(transcript)

        return result

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Voice itinerary generation failed: {exc}",
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            
@router.get("/itinerary/{trip_id}/audio")
async def get_itinerary_audio(
    trip_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    output_path = None

    try:
        # Get the itinerary belonging to this authenticated user
        result = get_itinerary_by_trip(
            session,
            trip_id,
            current_user.id,
        )

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Itinerary not found for this trip",
            )

        # Convert itinerary into text for TTS
        speech_parts = [
            "Here is your travel itinerary."
        ]

        for day in result.itinerary:
            speech_parts.append(
                f"Day {day.day}."
            )

            for activity in day.activities:
                speech_parts.append(activity)

        speech_text = " ".join(speech_parts)

        # Create temporary MP3 file
        output_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3",
        )

        output_path = output_file.name
        output_file.close()

        # Text → Speech
        await text_to_speech(
            speech_text,
            output_path,
        )

        # Return audio
        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            filename="trip_itinerary.mp3",
        )

    except HTTPException:
        raise

    except Exception as exc:
        if output_path and os.path.exists(output_path):
            os.remove(output_path)

        raise HTTPException(
            status_code=500,
            detail=f"Itinerary audio generation failed: {exc}",
        )