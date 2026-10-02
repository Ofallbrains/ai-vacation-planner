from langchain_anthropic import ChatAnthropic
from typing import Any
from app.config import settings
from app.graph.travel_graph import travel_graph


def run_agent(user_request: str | list[dict[str, Any]]):
    result = travel_graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_request,
                }
            ],
            "final_response": None,
        }
    )

    return result["final_response"]