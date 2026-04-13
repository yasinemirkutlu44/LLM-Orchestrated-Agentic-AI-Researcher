import asyncio

import gradio as gr
from dotenv import load_dotenv
from LLM_Orchestrator import Orchestrator
from query_validator_agent import query_validator_agent
from agents import Runner

load_dotenv(override=True)


async def run(query: str, progress=gr.Progress()):

    # Build a no-op yield that leaves UI unchanged
    no_change = (
        gr.update(),   # report
        gr.update(),   # pdf_file
        gr.update(),   # run_button
        gr.update(),   # restart_button
        gr.update(),   # query_textbox
    )

    # Validate query before proceeding
    if not query.strip() or not query:
        gr.Warning("Please enter a valid research query before clicking Search button.")
        yield no_change
        return
    if len(query.strip().split()) < 3:
        gr.Warning("Please enter a more detailed research query (at least 3 words) before clicking Search button.")
        yield no_change
        return
    validation_results = await Runner.run(query_validator_agent, query)
    validation = validation_results.final_output
    if not validation.is_valid:
        gr.Warning(f"Query is not valid: {validation.reason}")
        yield no_change
        return

    stage_progress = {
    "Search plan generated, performing searches...": (0.2, "Performing searches..."),
    "Searches completed, writing report...": (0.5, "Writing report..."),
    "Report written, saving as PDF...": (0.75, "Saving PDF..."),
    "Report written and saved as PDF, research complete": (0.95, "Finalising..."),
}

    progress(0.0, desc="Starting research")
    last_text, last_pdf = "", None
    # Immediately disable textbox + Run button, keep Restart disabled
    yield (
        "",                              # report cleared
        None,                            # pdf_file cleared
        gr.update(interactive=False),    # run_button
        gr.update(interactive=False),    # restart_button
        gr.update(interactive=False),    # query_textbox (keeps its value, locked)
    )
    async for chunk in Orchestrator().operate(query):
        text, pdf_path = chunk
        last_text, last_pdf = text, pdf_path

        print(f">>> yielded text: {text!r}")
        if text in stage_progress:
            pct, desc = stage_progress[text]
            print(f">>> progress match → {pct}")
            progress(pct, desc=desc)
        else:
            print(">>> NO MATCH")
                 
        yield (
            text,
            pdf_path,
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
        )
    # Done: enable Restart, keep Run + textbox disabled
    #progress(1.0, desc="Research completed")
    yield (
        last_text,
        last_pdf,
        gr.update(interactive=False),
        gr.update(interactive=True),
        gr.update(interactive=False),
    )
    
    await asyncio.sleep(0.5)
    progress(1.0, desc="Research completed")

def restart():
    return (
        gr.update(value="", interactive=True),   # query_textbox cleared + enabled
        "",                                       # report cleared
        None,                                     # pdf_file cleared
        gr.update(interactive=True),              # run_button re-enabled
        gr.update(interactive=False),             # restart_button disabled
    )


with gr.Blocks(theme=gr.themes.Default(primary_hue="green")) as ui:
    gr.Markdown("# 🔬 LLM-Orchestrated Agentic AI Researcher 📚")
    gr.Markdown(
        "Enter any research topic and the researcher will plan a search strategy, "
        "run multiple parallel web searches, synthesise the findings into a structured "
        "report, and deliver it as a downloadable PDF. Powered by an orchestration of "
    "specialised LLM agents, each handling a unique task in the workflow."
    )
    gr.Markdown(
    "<span style='font-size: 0.96em; opacity: 0.8;'>"
    "🧠 Built with OpenAI frontier models and the OpenAI Agents SDK 🚀."
    "</span>"
)
    
    query_textbox = gr.Textbox(
        label="Please type your research query here:",
        placeholder="e.g., What are the latest advancements in Large Language Models for healthcare applications?",
        info="Please be specific. A good query leads to a better report.",
    )
    with gr.Row():
        run_button = gr.Button("Search", variant="primary")
        restart_button = gr.Button("Restart", variant="secondary", interactive=False)
    report = gr.Markdown(label="Report")
    pdf_file = gr.File(label="Download PDF Report")

    run_outputs = [report, pdf_file, run_button, restart_button, query_textbox]
    run_button.click(fn=run, inputs=query_textbox, outputs=run_outputs)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=run_outputs)

    restart_button.click(
        fn=restart,
        inputs=None,
        outputs=[query_textbox, report, pdf_file, run_button, restart_button],
    )

ui.launch(inbrowser=True)