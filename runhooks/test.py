from agents import Agent, Runner, RunHooks, function_tool , tool ,RunConfig ,OpenAIChatCompletionsModel ,AsyncOpenAI
from dotenv import load_dotenv
import asyncio 
load_dotenv()
import nest_asyncio
nest_asyncio.apply()

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool()
def  add(a: int ,b:int): 
    "add two numbers"
    return a+b 


example=Agent(name = "example_agent",
    instructions="this is an example agent ",
    tools=[add]
)

output=Runner.run_sync(example , input="what is 2 plus 2 ?", context=None)
print(output.final_output)