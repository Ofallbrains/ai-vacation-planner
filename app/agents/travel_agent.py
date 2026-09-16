from langchain_anthropic import ChatAnthropic

from app.config import settings
from app.graph.travel_graph import travel_graph


def run_agent(user_request: str):
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