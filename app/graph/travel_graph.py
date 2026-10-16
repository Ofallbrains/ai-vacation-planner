from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from app.services.state import TravelState
from app.services.llm import model
from app.tools.weather_tool import get_weather
from app.tools.rag_tool import search_travel_knowledge
from app.schemas.ai_response import AIItineraryResponse


tools = [
    get_weather,
    search_travel_knowledge,
]

model_with_tools = model.bind_tools(tools)

structured_model = model.with_structured_output(
    AIItineraryResponse
)

def call_model(state: TravelState):
    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response],
    }

def generate_final_itinerary(state: TravelState):
    response = structured_model.invoke(
        state["messages"]
    )

    return {
        "final_response": response,
    }

tool_node = ToolNode(tools)

graph_builder = StateGraph(TravelState)

graph_builder.add_node(
    "agent",
    call_model,
)

graph_builder.add_node(
    "tools",
    tool_node,
)

graph_builder.add_node(
    "final",
    generate_final_itinerary,
)

graph_builder.add_edge(
    START,
    "agent",
)

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: "final",
    },
)

graph_builder.add_edge(
    "tools",
    "agent",
)

graph_builder.add_edge(
    "final",
    END,
)

travel_graph = graph_builder.compile()