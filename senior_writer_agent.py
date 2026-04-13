from agents import Agent
from pydantic import BaseModel, Field


writer_agent_instructions = """
You are a senior researcher responsible for producing a cohesive, well-structured report in response to a research query. 
You will receive the original query along with preliminary findings gathered by a research assistant.
Begin by drafting an outline that lays out the structure and narrative flow of the report. 
Once the outline is in place, write the full report based on it and return that as your final output.
The report must be in markdown format and should be substantial in both length and depth — 
Your must produce roughly 3–6 pages of content and the content should not be fewer than 1,500 words."""

#Pydantic models for the writer agent's output

class ReportOutline(BaseModel):
    summary: str = Field(description="A brief summary of the main findings and conclusions that the report will present.")

    report: str = Field(description="The full markdown body of the report, structured according to the outline and incorporating the research assistant's findings.")

    suggested_questions: list[str] = Field(description="A list of any additional questions that should be explored to deepen the report, based on gaps or interesting leads in the research assistant's findings.")

writer_agent = Agent(
    name="Report Writer",
    instructions=writer_agent_instructions,
    model="gpt-4.1-mini",
    output_type=ReportOutline,
)

print("Report Writer agent created successfully.")