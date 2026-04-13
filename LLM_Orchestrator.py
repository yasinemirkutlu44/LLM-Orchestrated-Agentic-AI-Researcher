
from agents import Runner
import asyncio
from agents import trace
from research_assistant_agent import research_assistant_agent
from searchplanner_agent_researcher import WebSearchItem, WebSearchPlan, searchplanner_agent
from senior_writer_agent import writer_agent
from PDF_creator_agent import _save_pdf_report_impl


class Orchestrator:

    async def operate(self, query: str):
        with trace("Deep Research Agentic AI"):
            print("Planning searches...")
            search_plan = await self.search_planner(query)
            yield "Search plan generated, performing searches...", None
            search_results = await self.do_search(search_plan)
            yield "Searches completed, writing report...", None
            report_markdown = await self.write_report(query, search_results)
            yield "Report written, saving as PDF...", None
            #await asyncio.sleep(0.5) # small delay to ensure UI updates before PDF generation
            pdf_path = await self.save_as_pdf(report_markdown)
            yield "Report written and saved as PDF, research complete", None
            #await asyncio.sleep(0.5)  # small delay to ensure UI updates before final output
            yield report_markdown, pdf_path

    async def search_planner(self, query: str) -> WebSearchPlan:
        """Use the search planner agent to generate a web search plan for a given query."""
        print(f"Planning Searchers. Generating search plan for query: {query}")
        results = await Runner.run(searchplanner_agent, f"Query: {query}")
        return results.final_output

    async def do_search(self, search_plan: WebSearchPlan) -> list[str]:
        """Use the research assistant agent to perform web searches based on a search plan."""
        #print(f"Performing Searches. Executing search plan: {search_plan.searches}")
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = await asyncio.gather(*tasks)
        print(f"Searches completed. Results: {results}")
        return results

    async def search(self, item: WebSearchItem) -> str:
        """Perform a single web search using the research assistant agent."""
        print(f"Performing Search. Searching for: {item}")
        input = f"Search term: {item.query} and Search rationale: {item.reason}"
        result = await Runner.run(research_assistant_agent, input)
        print(f"Search completed for '{item}'. Result: {result}")
        return result.final_output
    
    async def write_report(self, query: str, search_results: list[str]):
        """Run the writer agent and return the report markdown."""
        print("Thinking about report...")
        writer_input = f"Original query: {query}\nSummarized search results: {search_results}"
        writer_result = await Runner.run(writer_agent, writer_input)
        report_data = writer_result.final_output
        print("Finished writing report")
        return report_data.report
    
    async def save_as_pdf(self, report_markdown: str) -> str:
        """Save the given markdown report as a PDF and return the file path."""
        print("Saving report as PDF...")
        first_line = report_markdown.strip().split("\n", 1)[0]
        title = first_line.lstrip("#").strip() or "Research Report"
        result = _save_pdf_report_impl(title, report_markdown)
        pdf_path = result["filepath"]
        print(f"PDF saved. Path: {pdf_path}")
        return pdf_path
    
    async def produce_pdf_report(self, query: str, search_results: list[str]):
        print("Thinking about report...")
        writer_input = f"Original query: {query}\nSummarized search results: {search_results}"
        writer_result = await Runner.run(writer_agent, writer_input)
        report_data = writer_result.final_output
        print("Finished writing report")

        print("Saving report as PDF...")
        first_line = report_data.report.strip().split("\n", 1)[0]
        title = first_line.lstrip("#").strip() or "Research Report"

        result = _save_pdf_report_impl(title, report_data.report)
        pdf_path = result["filepath"]
        print(f"PDF saved. Path: {pdf_path}")

        return report_data.report, pdf_path
