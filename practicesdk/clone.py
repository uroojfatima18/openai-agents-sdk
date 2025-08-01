from agents import Agent, function_tool,OpenAIChatCompletionsModel, RunConfig,AsyncOpenAI,Runner,handoff,RunContextWrapper
import asyncio
from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
import os
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
burger_recipe= Agent(
    name="Burger recipe",
    instructions="You are a burger recipe agent, write a recipe in haiku form",)

pizza_recipe = Agent(
    name="pizza agent",
    instructions="You are a pizza recipe agent, write a recipe in haiku form",)

# clone for burger_recipe behaivour change not for  main agent change
order_billing=burger_recipe.clone(
    name="recipe agent",             # i call this clone method when i want this agent behaviour like robot
    instructions="write recipe like a robot in haiku form")

handoff_agent = Agent(
    name="Handoff agent",   
    instructions="You are a handoff agent, you will handle the handoff of burger and pizza recipes",
    handoffs=[order_billing,pizza_recipe])

result= Runner.run_sync (handoff_agent,input="give burger recipe", run_config=run_config)

print(result.final_output)
print(result.last_agent.name)