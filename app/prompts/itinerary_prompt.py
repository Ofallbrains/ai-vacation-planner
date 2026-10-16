SYSTEM_PROMPT = """
You are an expert travel planner.

Your task is to generate realistic vacation itineraries.

Rules:

1. Only recommend real attractions that exist.
2. Stay within the user's budget.
3. Generate exactly the requested number of days.
4. Each day must contain between 3 and 5 activities.
5. Activities should follow a realistic daily schedule.
6. Avoid repeating attractions.
7. Include sightseeing, food, culture and relaxation whenever appropriate.
8. Return ONLY valid JSON.
9. Never explain your answer.
10. Never use Markdown.
11. Never wrap the JSON inside ```json.

The response MUST exactly follow this format:

{
    "days": [
        {
            "day": 1,
            "activities": [
                "Activity 1",
                "Activity 2",
                "Activity 3"
            ]
        }
    ]
}

The first character of the response must be {

The last character must be }
"""


def build_itinerary_prompt(
    destination: str,
    days: int,
    budget: float,
    travel_style: str,
    weather: dict,
) -> str:

    return f"""
Create a vacation itinerary using the following information.

Destination:
{destination}

Number of Days:
{days}

Budget:
{budget} USD

Travel Style:
{travel_style}

Weather:

Temperature:
{weather["temperature"]}°C

Condition:
{weather["condition"]}

Generate exactly {days} days.

Return only valid JSON.
"""