from typing import Annotated

from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from app.schemas.ai_response import AIItineraryResponse
class TravelState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    final_response: AIItineraryResponse | None