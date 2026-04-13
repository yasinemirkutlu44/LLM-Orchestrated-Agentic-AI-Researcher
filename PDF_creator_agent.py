from datetime import datetime
from pathlib import Path
from typing import Dict
from agents import Agent, function_tool
from markdown_pdf import MarkdownPdf, Section

def _save_pdf_report_impl(title: str, markdown_body: str) -> Dict[str, str]:
    """Plain function that does the actual PDF saving."""
    project_dir = Path.cwd()
    reports_dir = project_dir / "reports"
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title).strip().replace(" ", "_")
    filepath = reports_dir / f"{safe_title}_{timestamp}.pdf"

    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00a0": " ",
        "\u2212": "-", "\u2022": "*",
    }
    clean_body = markdown_body
    for fancy, plain in replacements.items():
        clean_body = clean_body.replace(fancy, plain)

    pdf = MarkdownPdf(toc_level=0)
    pdf.add_section(Section(clean_body))
    pdf.meta["title"] = title
    pdf.save(str(filepath))
    print(f"PDF saved to: {filepath.resolve()}")
    return {"status": "success", "filepath": str(filepath.resolve())}

@function_tool
def save_pdf_report(title: str, markdown_body: str) -> Dict[str, str]:
    return _save_pdf_report_impl(title, markdown_body)

pdf_agent_instructions = """
You save research reports as PDFs. You will receive a markdown report.
   You MUST call the save_pdf_report tool exactly once, passing:
   - title: a short descriptive title derived from the report's actual H1 heading
   - There must be only one H1 heading in the markdown, and it must be the first line. If there is no H1 heading, or if there are multiple, respond with an error instead of inventing a title.
   - markdown_body: the EXACT markdown you received, character-for-character, with no edits, no rewrites, no summarization, no substitution, no invented content
   Do NOT generate your own report. Do NOT use placeholder examples. If the input is empty, respond with an error instead of inventing content.
   Use only plain ASCII punctuation: straight quotes, hyphens, and standard dashes — no em dashes, en dashes, or curly quotes.
"""


pdf_agent = Agent(
    name="PDF Report Saver",
    instructions=pdf_agent_instructions,
    tools=[save_pdf_report],
    model="gpt-4.1-mini",
)

print("PDF Report Saver agent created successfully.")