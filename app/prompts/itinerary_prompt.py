SYSTEM_PROMPT = """
You are an AI vacation planning assistant.

Create practical and personalized travel itineraries.

Use the provided trip information, weather information, and
retrieved travel knowledge when creating the itinerary.

The retrieved travel knowledge is supporting information from
the application's travel knowledge base.

Do not invent facts when relevant information is available
in the retrieved context.

Return ONLY valid JSON in this format:

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
    context: str,
) -> str:

    return f"""
Create a {days}-day travel itinerary for {destination}.

Trip information:
- Destination: {destination}
- Number of days: {days}
- Budget: {budget}
- Travel style: {travel_style}

Current weather information:
- Temperature: {weather.get("temperature")}°C
- Condition: {weather.get("condition")}

Retrieved travel knowledge:
{context}

Instructions:
1. Create an itinerary for every day.
2. Consider the traveler's budget and travel style.
3. Consider the provided weather conditions.
4. Use relevant information from the retrieved travel knowledge.
5. Prefer attractions, neighborhoods, food, and activities
   supported by the retrieved knowledge when appropriate.
6. Do not mention the retrieval process in the response.
7. Return ONLY valid JSON.

The response must follow this structure:

{{
    "days": [
        {{
            "day": 1,
            "activities": [
                "Activity 1",
                "Activity 2"
            ]
        }}
    ]
}}
"""