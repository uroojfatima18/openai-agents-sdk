import asyncio

from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace
import agentops
from agents import Agent, function_tool,OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI,Runner,handoff,RunContextWrapper
from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
import os
from pydantic import BaseModel

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
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
"""
This example shows the agents-as-tools pattern. The frontline agent receives a user message and
then picks which agents to call, as tools. In this case, it picks from a set of translation
agents.
"""

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    handoff_description="An english to french translator",
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    handoff_description="An english to italian translator",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        """You are a translation coordinator. You never translate yourself."
        "Use the correct tools to translate based on user request. "
        "If multiple languages are mentioned, use the matching tools one by one"""
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
    ],
)
synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You are a proofreader. Take the translated outputs and clean/merge them into a final response",
)
api_key="fa56d1a5-1b65-45d4-b2b3-a8c0fe444f2f"

agentops.init(api_key)
async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    # Run the entire orchestration in a single trace
    with trace("Orchestrator evaluator"):
        orchestrator_result = await Runner.run(orchestrator_agent, msg,run_config=run_config)

        for item in orchestrator_result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f"  - Translation step: {text}")

        synthesizer_result = await Runner.run(
            synthesizer_agent, orchestrator_result.to_input_list(), run_config=run_config,
        )

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")

# async def main():
#     result = await Runner.run(orchestrator_agent, "Translate 'Hello, how are you?' to Spanish",run_config=run_config)
#     print(result.final_output)

# asyncio.run(main())
if __name__ == "__main__":
    asyncio.run(main())