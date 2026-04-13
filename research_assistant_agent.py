from agents import Agent, ModelSettings, WebSearchTool


RA_INSTRUCTIONS = """You are a research assistant. When given a search term, perform a web search on it and return a brief summary of what you find.
Your summary should be 2–3 paragraphs and remain below 300 words, focusing on the key points and core findings. 
Prioritise density over polish—full sentences and perfect grammar aren't necessary. 
Your output will feed into a larger report being assembled by someone else, so strip out filler and surface only the substance. 
Return the summary alone, with no preamble, commentary, or closing remarks."""

research_assistant_agent = Agent(
    name="Research Assistant",
    instructions=RA_INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4.1-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

print("Research Assistant agent created successfully.")