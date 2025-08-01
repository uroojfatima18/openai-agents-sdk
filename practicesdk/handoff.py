from agents import Agent, function_tool,OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI,Runner,handoff,RunContextWrapper
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

class EscalationData(BaseModel):
    reason: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):   #context 
    print(f"Escalation agent called with reason: {input_data.reason}")


billing_agent = Agent(
    name="Billing Agent",
    instructions="You are a billing agent, make bills of customer"
)
refund_agent=Agent(
    name="refund_agent",
    instructions="you are a refund agent, help customer ot refund their amount"
)
# def on_handoff(ctx:RunContextWrapper):
#     print("on handoffs called!")
agent = Agent(name="Escalation agent")

billing_handoff = handoff(
    agent=agent, 
    on_handoff=on_handoff
print(result.final_output)
)            
triage_agent = Agent(
    name="Triage agent",
    handoffs=[billing_handoff,refund_agent],
)
class CurrentUser(BaseModel):
    is_logged_in: bool = False
async def can_customer_refund(local_context:RunContextWrapper[CurrentUser],agent:Agent[CurrentUser])-> bool:
    print("Local context:", local_context)
    if local_context.context and local_context.context.is_logged_in:
        return True 
    return False

    # Here you can implement your logic to determine if the customer can refund
current_user = CurrentUser(is_logged_in=True)  # if true user is loging refund agent call otherwise general agent will be called

 is_enabled= can_customer_refund)


