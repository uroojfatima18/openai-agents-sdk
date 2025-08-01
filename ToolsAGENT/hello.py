
import os
import asyncio
import requests
from agents.tool import function_tool
from dotenv import load_dotenv
from agents import Agent, RunConfig, set_tracing_disabled, OpenAIChatCompletionsModel, AsyncOpenAI, Runner
from agents.extensions.models.litellm_model import LitellmModel

# Environment setup
load_dotenv()

set_tracing_disabled(disabled=True)

# Get API key from userdata
api_key = os.getenv('GEMINI_API_KEY')

# Setup external client
provider = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define the model
MODEL = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)
run_config = RunConfig(
    model=MODEL,
    model_provider=provider,
    tracing_disabled=True
)

# Define agents
agent2 = Agent(
    name="Web Development Assistant",
    instructions="You are a web development expert. Help users with web development queries.",
    model=MODEL,
)

agent3 = Agent(
    name="App Development Assistant",
    instructions="You are an app development expert. Help users with app development queries.",
    model=LitellmModel(model=MODEL, api_key= api_key,
))


agent5 = Agent(
    name="Backend Developer Assistant",
    instructions="You are a backend development expert. Help users with backend development queries.",
    model=LitellmModel(model=MODEL, api_key= api_key,
))

agent6 = Agent(
    name="DevOps Developer Assistant",
    instructions="You are a DevOps expert. Help users with DevOps-related queries.",
    model=LitellmModel(model=MODEL, api_key= api_key,
))

agent4 = Agent(
    name="AI Agent",
    instructions="You are an AI expert. Help users with AI-related queries.",
    model=LitellmModel(model=MODEL, api_key= api_key),
    tools=[
        agent5.as_tool(tool_name="Backend Developer Tool", tool_description="Helps with backend queries."),
        agent6.as_tool(tool_name="DevOps Developer Tool", tool_description="Helps with DevOps queries."),
    ],
)

# Setup tools
web_development_tool = agent2.as_tool(
    tool_name="Web Development Tool",
    tool_description="Helps with web development queries."
)

app_development_tool = agent3.as_tool(
    tool_name="App Development Tool",
    tool_description="Helps with app development queries."
)

ai_agent_tool = agent4.as_tool(
    tool_name="AI Agent Tool",
    tool_description="Helps with AI-related queries."
)

# Main agent
agent1 = Agent(
    name="Panacloud Assistant",
    instructions="You are a Panacloud expert helping with course-related queries.",
    model=LitellmModel(model=MODEL, api_key= api_key),
    tools=[web_development_tool, app_development_tool, ai_agent_tool],
)

# Run and print
import asyncio

result = asyncio.run(
    Runner.run(
        starting_agent=agent1,
        input="What are the courses offered by PIAIC"
    )
)
async def main(input_text: str):
    result = await Runner.run(agent1, input=input_text, run_config=run_config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main("How many handoffs do you have? Also tell Which Agent Have Agents As A Tool name it also"))

# # Print the results
# print(result.last_agent.name)
# print(result.final_output)
