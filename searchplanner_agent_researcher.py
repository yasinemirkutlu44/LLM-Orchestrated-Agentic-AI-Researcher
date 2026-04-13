from agents import Agent
from pydantic import BaseModel, Field


number_of_searches = 2


searchplanner_agent_instructions = f"""
You are a helpful research assistant. Given a user's query, your job is to plan the research by generating a set of targeted web searches that together will yield the information needed to answer it well. 
Produce exactly {number_of_searches} search terms, each one focused on a distinct angle or sub-topic of the query so the results complement rather than duplicate each other.
 Return only the list of search terms, with no explanations or extra commentary.
"""

class WebSearchItem(BaseModel):
    query: str = Field(description="The search term to use.")
    reason: str = Field(description="A brief explanation of why this search is useful.")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="A list of web searches to perform to best answer the user's query."
    )

searchplanner_agent = Agent(
    name="Search Planner",
    instructions=searchplanner_agent_instructions,
    model="gpt-4.1-mini",
    output_type=WebSearchPlan,
)