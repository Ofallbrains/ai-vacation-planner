
from unittest.mock import patch

from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.travel_agent import run_agent
from app.prompts.itinerary_prompt import SYSTEM_PROMPT


def test_agent_receives_system_prompt():

    with patch(
        "app.agents.travel_agent.travel_graph.invoke"
    ) as mock_invoke:

        mock_invoke.return_value = {
            "final_response": "test response"
        }

        result = run_agent("Plan a vacation in Kenya")

        assert result == "test response"

        graph_input = mock_invoke.call_args.args[0]
        messages = graph_input["messages"]

        assert isinstance(messages[0], SystemMessage)
        assert messages[0].content == SYSTEM_PROMPT

        assert isinstance(messages[1], HumanMessage)
        assert messages[1].content == "Plan a vacation in Kenya"
