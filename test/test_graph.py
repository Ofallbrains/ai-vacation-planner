from app.graph.travel_graph import travel_graph


def test_travel_graph():
    result = travel_graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Plan a 3-day trip to Paris. "
                        "Check the weather and use travel "
                        "knowledge to recommend activities."
                    ),
                }
            ],
            "final_response": None,
        }
    )

    print("\n========== LANGGRAPH EXECUTION ==========")

    for message in result["messages"]:
        print("\nMESSAGE TYPE:", type(message).__name__)
        print(message)

    print("\n========== FINAL RESPONSE ==========")
    print(result["final_response"])

    assert result["final_response"] is not None
    assert len(result["final_response"].days) == 3