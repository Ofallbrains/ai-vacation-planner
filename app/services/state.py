from dataclasses import dataclass

@dataclass
class AIState:
    destination: str
    days: int
    budget: float
    travel_style: str
    weather: dict