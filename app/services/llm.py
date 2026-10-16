from langchain_anthropic import ChatAnthropic

from app.config import settings

model = ChatAnthropic(
    model=settings.anthropic_model,
    api_key=settings.anthropic_api_key,
    temperature=0.7,
)