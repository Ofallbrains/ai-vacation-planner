import logging
from typing import Any

logger = logging.getLogger(__name__)

MODEL_PRICING = {
    "claude-haiku-4-5-20251001": {
        "input": 1.00,
        "output": 5.00,
    },
    "claude-haiku-4-5": {
        "input": 1.00,
        "output": 5.00,
    },
}


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    input_price: float,
    output_price: float,
) -> float:
    """Calculate estimated LLM cost in USD."""

    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price

    return input_cost + output_cost


def track_token_usage(usage: dict[str, Any]) -> None:
    """Log token consumption and estimated cost for each model."""

    if not usage:
        logger.warning("No LLM token usage metadata was returned.")
        return

    for model_name, token_data in usage.items():
        input_tokens = token_data.get("input_tokens", 0)
        output_tokens = token_data.get("output_tokens", 0)
        total_tokens = token_data.get("total_tokens", 0)

        pricing = MODEL_PRICING.get(model_name)

        if pricing is None:
            logger.info(
                "LLM usage | model=%s | input=%s | output=%s | "
                "total=%s | cost=not configured",
                model_name,
                input_tokens,
                output_tokens,
                total_tokens,
            )
            continue

        estimated_cost = calculate_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_price=pricing["input"],
            output_price=pricing["output"],
        )

        logger.info(
            "LLM usage | model=%s | input=%s | output=%s | "
            "total=%s | estimated_cost=$%.8f",
            model_name,
            input_tokens,
            output_tokens,
            total_tokens,
            estimated_cost,
        )