from app.observability.cost_tracker import track_token_usage
from fastapi import logger
from langchain_anthropic import ChatAnthropic
from typing import Any
from app.config import settings
from app.graph.travel_graph import travel_graph
from langchain_core.messages import HumanMessage, SystemMessage
from app.prompts.itinerary_prompt import SYSTEM_PROMPT
from langchain_core.callbacks import UsageMetadataCallbackHandler

def run_agent(user_request: str | list[dict[str, Any]]):
    usage_callback = UsageMetadataCallbackHandler()
    
    logger.info("Starting travel agent execution")
    
    
    result = travel_graph.invoke(
        {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_request),
            ],
            "final_response": None,
        },
        config={
            "callbacks": [usage_callback]
        }
    )
    
    usage = usage_callback.usage_metadata   

    track_token_usage(usage)

    logger.info("Travel agent execution completed")

    return result["final_response"]