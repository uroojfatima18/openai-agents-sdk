from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal
from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
from agents import Agent, ItemHelpers, Runner, TResponseInputItem, trace, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI,enable_verbose_stdout_logging
import os
import agentops 

# enable_verbose_stdout_logging()
"""
This example shows the LLM as a judge pattern. The first agent generates an outline for a story.
The second agent judges the outline and provides feedback. We loop until the judge is satisfied
with the outline.
"""
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

Model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)
run_config =RunConfig(
    model=Model,
    model_provider=external_client,
)
story_outline_generator = Agent(
    name="story_outline_generator",
    instructions=(
        "You generate a very short story outline based on the user's input."
        "If there is any feedback provided, use it to improve the outline."
    ),
)

@dataclass
class EvaluationFeedback:
    feedback: str
    score: Literal["pass", "needs_improvement", "fail"]

# agent as judge
evaluator = Agent(
    name="evaluator",
    instructions=(
        "You evaluate a story outline and decide if it's good enough."
        "If it's not good enough, you provide feedback on what needs to be improved."
        "Never give it a pass on the first try. After 3 attempts, you can give it a pass if story outline is good enough - do not go for perfection"
    ),
    output_type=EvaluationFeedback,
)
async def main() -> None:
    msg = input("What kind of story would you like to hear? ")
    input_items: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    latest_outline: str | None = None

    # We'll run the entire workflow in a single trace
    with trace("LLM as a judge"):
        while True:
            story_outline_result = await Runner.run(
                story_outline_generator,
                input_items,
                run_config=run_config,
            )

            input_items = story_outline_result.to_input_list()
             #input_list-works ->1 agent ka ouput lkr dosre agen k lie input banata ha uc structed m jisme agent smjhta 
            latest_outline = ItemHelpers.text_message_outputs(story_outline_result.new_items)
            print("Story outline generated")

            evaluator_result = await Runner.run(evaluator, input_items,run_config=run_config)
            result: EvaluationFeedback = evaluator_result.final_output

            print(f"Evaluator score: {result.score}")

            if result.score == "pass":
                print("Story outline is good enough, exiting.")
                break

            print("Re-running with feedback")

            input_items.append({"content": f"Feedback: {result.feedback}", "role": "user"})

    print(f"Final story outline: {latest_outline}")


if __name__ == "__main__":
    asyncio.run(main())