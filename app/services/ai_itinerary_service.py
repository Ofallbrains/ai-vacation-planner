import json
from anthropic import Anthropic

from app.config import settings

client = Anthropic(
    api_key=settings.anthropic_api_key
)


def generate_itinerary(
    destination: str,
    days: int,
    budget: float,
    travel_style: str
):

    prompt = f"""
You are a professional vacation planning assistant.

Create a detailed itinerary based on the following trip:

Destination: {destination}
Number of Days: {days}
Budget: {budget} USD
Travel Style: {travel_style}

Rules:

1. Only include attractions and activities that exist in {destination}.
2. Keep recommendations within the stated budget.
3. Create exactly {days} days.
4. Each day should contain 3-5 activities.
5. Activities should follow a realistic schedule.
6. Avoid duplicate attractions.
7. Include a mix of sightseeing, food, culture and relaxation when appropriate.
8. Return ONLY JSON.
9. Do not include markdown.
10. Do not explain your answer

Return:

{{
  "days":[
    {{
      "day":1,
      "activities":[
        "activity",
        "activity"
      ]
    }}
  ]
}}
"""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    

    result = response.content[0].text.strip()

    try:
        
        return json.loads(result)
    except Exception:
        raise Exception(
            f"Claude returned invalid JSON:\n{result}"
        )