from agents import Agent
from pydantic import BaseModel, Field

class QueryValidationInput(BaseModel):
    is_valid: bool
    reason: str 

query_validator_instructions = """
You are a helpful assistant that validates user queries for a research agent.
Your task is to determine if a given research query is valid and actionable for the research agent.
Given a user's query, decide if it's a meaningful 
research question that can be answered with web searches. Return is_valid=False for gibberish, single unrelated words, or clearly nonsensical input. Return "
is_valid=True for any genuine question or topic, even if broad. Provide a brief reason.
"""

query_validator_agent = Agent(
    name="Query Validator",
    instructions=query_validator_instructions,
    model="gpt-4.1-mini",
    output_type=QueryValidationInput,
)

print("Query Validator agent created successfully.")