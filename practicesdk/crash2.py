from agents import Agent, function_tool,OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI,Runner,handoff,RunContextWrapper
from agents.agent import ModelSettings, StopAtTools
from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
import os
import asyncio
import agentops
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
    tracing_disabled=True
)


@function_tool
def weather(city:str)->str:
    " your'e a weather agent, you can provide weather information for a given city."
    return f"Weather in {city} is sunny."

@function_tool
def support(city:str)->str:
    "you are a support agent, you can provide support information for a given city."
    return f"support details of  {city} there:  1234567"


async def main():
    agent = Agent(
        name="Assistant",
        instructions="you are a helpful assistant respnse in haiku form ",
        tools=[weather,support ], # add tools here
        model=Model,
        # tool_use_behavior=StopAtTools(stop_at_tool_name="weather"),  # stop at weather tool
        model_settings=ModelSettings(tool_choice= "none",parallel_tool_calls=True),       
        # reset_tool_choice=True,  # reset tool choice after each run)
    )
    result = await Runner.run(
        agent,
        input="what is the weather in karachi and what is the support number of lahore there?",
        run_config=run_config
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())