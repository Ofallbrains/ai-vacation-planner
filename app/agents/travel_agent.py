from langchain_anthropic import ChatAnthropic
from typing import Any
from app.config import settings
from app.graph.travel_graph import travel_graph
from langchain_core.messages import HumanMessage, SystemMessage
from app.prompts.itinerary_prompt import SYSTEM_PROMPT

def run_agent(user_request: str | list[dict[str, Any]]):
    result = travel_graph.invoke(
        {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_request),
            ],
            "final_response": None,
        }
    )

    return result["final_response"]