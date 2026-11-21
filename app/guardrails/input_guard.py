
import math
import re


class InputGuardError(ValueError):
    """Raised when a travel request fails security validation."""


# Common prompt injection patterns.
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions",
    r"override\s+(the\s+)?system\s+prompt",
    r"reveal\s+(your\s+)?(system\s+prompt|api\s+key|credentials)",
    r"show\s+(me\s+)?(your\s+)?(system\s+prompt|api\s+key)",
    r"act\s+as\s+if\s+you\s+have\s+no\s+restrictions",
    r"bypass\s+(your\s+)?(security|safety|guardrails)",
]


def detect_prompt_injection(text: str) -> bool:
    """Detect common attempts to override trusted instructions."""

    if not isinstance(text, str):
        return False

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def validate_trip_input(
    destination: str,
    days: int,
    budget: float,
    travel_style: str,
) -> None:
    """Validate travel details before sending them to the AI agent."""

    # 1. Validate destination
    if not isinstance(destination, str):
        raise InputGuardError("Destination must be text.")

    destination = destination.strip()

    if not destination:
        raise InputGuardError("Destination cannot be empty.")

    if len(destination) > 100:
        raise InputGuardError("Destination is too long.")

    # 2. Validate number of days
    if isinstance(days, bool) or not isinstance(days, int):
        raise InputGuardError("Days must be a valid integer.")

    if not 1 <= days <= 30:
        raise InputGuardError(
            "Trip duration must be between 1 and 30 days."
        )

    # 3. Validate budget
    if isinstance(budget, bool) or not isinstance(budget, (int, float)):
        raise InputGuardError("Budget must be a valid number.")

    if not math.isfinite(budget) or budget < 0:
        raise InputGuardError(
            "Budget must be a finite, non-negative number."
        )

    # 4. Validate travel style
    if not isinstance(travel_style, str):
        raise InputGuardError("Travel style must be text.")

    travel_style = travel_style.strip()

    if not travel_style:
        raise InputGuardError("Travel style cannot be empty.")

    if len(travel_style) > 50:
        raise InputGuardError("Travel style is too long.")

    # 5. Check user-provided text for prompt injection
    user_text = f"{destination} {travel_style}"

    if detect_prompt_injection(user_text):
        raise InputGuardError(
            "Your request contains suspicious instructions "
            "that cannot be processed."
        )
