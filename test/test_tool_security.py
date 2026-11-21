
from app.graph.travel_graph import tools


def test_only_authorized_tools_are_available():

    allowed_tools = {
        "get_weather",
        "search_travel_knowledge",
    }

    actual_tools = {tool.name for tool in tools}

    assert actual_tools == allowed_tools


def test_unauthorized_tools_are_not_available():

    actual_tools = {tool.name for tool in tools}

    forbidden_tools = {
        "transfer_money",
        "book_flight",
        "execute_shell",
        "read_environment_variables",
    }

    assert actual_tools.isdisjoint(forbidden_tools)
