#100% run code with uv run app.py

import os
import nest_asyncio
from openai import AsyncOpenAI
from agents import  Agent, RunConfig, OpenAIChatCompletionsModel, set_tracing_disabled, AsyncOpenAI, Runner
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()
load_dotenv()
nest_asyncio.apply()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")

provider= AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL= OpenAIChatCompletionsModel(
    model="gemini-1.5-pro",
    openai_client=provider,
)



#web development agent
agent2=Agent(
    name="web development assistant",
    instructions="you are web development expert.Help user in webdeveopment queries",
    # model=OpenAIChatCompletionsModel(model=MODEL,openai_client=provider),
    model=MODEL,
    handoff_description="you only response to web development quaries",
)

#app development agent
agent3=Agent(
    name="App development assistant",
    instructions="you are app development expert.Help user in app deveopment queries",
    # model=OpenAIChatCompletionsModel(model=MODEL,openai_client=provider),
    model=MODEL,
    handoff_description="you only response to app development quaries"

)


#backend development agent
agent5=Agent(
    name="backend developer  assistant",
    instructions="you are backend developer expert.Help user in backend  deveopment queries",
    # model=OpenAIChatCompletionsModel(model=MODEL,openai_client=provider),
    model=MODEL,

)

#devops development agent
agent6 = Agent(
    name="devops developer assistant",
    instructions="you are devops developer expert. Help user in devops development queries",
    # model=OpenAIChatCompletionsModel(model=MODEL, openai_client=provider),
    model=MODEL,
)


# Backend development agent as tool
Backend_developer = agent5.as_tool(
    tool_name="backend developer assistant tool",  # Name of the tool
    tool_description="This tool helps with backend development queries."  # Description of the tool
)

#devops development agent as tool
devops_developer  = agent6.as_tool(
    tool_name="devops  developer assistant tool",  # Name of the tool
    tool_description="This tool helps with devops development queries."  # Description of the tool
)

#AI agent
agent4=Agent(
    name ="AI AGENT",
    instructions="you are AI AGENT expert",
    model =MODEL,
    handoff_description="you only response in AI AGENT related quaries",
    tools=[Backend_developer ,devops_developer ],
)


web_development_tool = agent2.as_tool(
    tool_name="web_development_assistant_tool",
    tool_description="This tool helps with web development queries."
)
app_development_tool = agent3.as_tool(
    tool_name="app_development_assistant_tool",
    tool_description="This tool helps with app development queries."
)

ai_agent_tool = agent4.as_tool(
    tool_name="ai_agent_tool",
    tool_description="This tool helps with AI-related queries."
)
agent1=Agent(
    name ="panacloud assistant",
    instructions="you are panacloud expert",
    # model =OpenAIChatCompletionsModel(model=MODEL,openai_client =provider),
    model=MODEL,
    handoff_description="you only response in AI AGENT related queries" ,
    tools=[web_development_tool, app_development_tool, ai_agent_tool],
)
import asyncio
result = asyncio.run(
    Runner.run(
        starting_agent=agent1,
        input="What are the courses offered by PIAIC"
    )
)
print(result.last_agent.name)
print(result.final_output)