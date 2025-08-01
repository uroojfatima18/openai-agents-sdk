
from agents import Agent, function_tool,OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI,Runner,handoff,RunContextWrapper,HandoffInputData
from agents.extensions import handoff_filters
from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
import os
import agentops
import asyncio
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
    tracing_disabled=True

)

def create_conversation_summary(handoff_input: HandoffInputData) -> HandoffInputData:
    """Creates a summary of the conversation instead of full history"""
    conversation = "\n".join([f"{msg.role}: {msg.content}" for msg in handoff_input.messages])
    
    # Generate summary (you can customize this logic)
    summary = f"""
    Conversation Summary:
    - Customer issue: {handoff_input.messages[-1].content}
    - Language detected: English
    - Key points: Customer needs assistance with their account
    """
    
    # Replace full history with summary
    handoff_input.messages = [
        {"role": "system", "content": summary}
    ]
    return handoff_input

# Define agents
english_agent = Agent(
    name="English Agent",
    instructions="You handle English customer queries. Here's the conversation summary: {{input}}",
    handoff_description="English language specialist"
)

# Create handoff with summary filter
english_handoff = handoff(
    agent=english_agent,
    input_filter=create_conversation_summary
)

# Create triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route customer to correct agent based on language",
    handoffs=[english_handoff, english_agent]
)

# Test the flow
result = Runner.run_sync(
    starting_agent=triage_agent,
    input="Hello, I  want you to write a essay for me for groming persanlity",
    run_config=run_config
)
print(result.final_output)
print("\n[Last Agent]", result.last_agent)