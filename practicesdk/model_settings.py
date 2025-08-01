from agents import Agent, function_tool,OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI,Runner,run_demo_loop,enable_verbose_stdout_logging

enable_verbose_stdout_logging()
from agents import Agent, ModelSettings
from agents.agent import StopAtTools 

from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
import os

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
@function_tool(name_override="weather")   # enable means tool not available for llm
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

@function_tool(name_override="weather_finder",is_enabled=False)
def get_support(city: str) -> str:
    return f"Support for {city} is available"

agent = Agent(
    name="",
    instructions="you are  a helpfull assistant",
    model="gemini-2.0-flash",
    tools=[get_weather,get_support],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_weather"]), 
    model_settings=ModelSettings(tool_choice="required",  # auto means llm will choose tool,
    # reset_tool_choice=True,  # reset tool choice after each run
    ))

result=Runner.run_sync(agent,input= "what is the weather in islamabad",run_config=run_config)
print(result.final_output)
