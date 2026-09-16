from app.agents.travel_agent import run_agent

def test_travel_agent():
    response = run_agent(
        """
        Plan a 2-day trip to Paris.

        Budget: 500
        Travel style: cultural

        Check the weather and use the travel knowledge base
        to choose suitable activities.
        """
        
    )
    
    print("\nAgent response:")
    print(response.model_dump_json(indent=2))
    assert isinstance(response.days, list)
    assert len(response.days) == 2
    assert all(day.activities for day in response.days)