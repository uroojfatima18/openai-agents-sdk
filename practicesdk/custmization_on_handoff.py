from agents import Agent, function_tool,OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI,Runner,handoff,RunContextWrapper
from agents.extensions import handoff_filters
from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
import os
import asyncio
from pydantic import BaseModel
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


)
# dynamic context for the agent
# this context will be passed to the agent when it is run
class CurrentUser(BaseModel):
    is_logged_in: bool = False

async def can_customer_refund(local_context:RunContextWrapper[CurrentUser],agent:Agent[CurrentUser])-> bool:
    print("Local context:", local_context)
    if local_context.context and local_context.context.is_logged_in:
        return True 
    return False
    # Here you can implement your logic to determine if the customer can refund

@function_tool
def weather(city:str)->str:
    " your'e a weather agent, you can provide weather information for a given city."
    return f"Weather in {city} is sunny."

# billing_agent = Agent(name="Billing agent")
refund_agent = Agent(name="Refund agent")

general_obj =Agent(
    name="general agent",
    tools=[weather],
    handoffs=[
        handoff(agent=refund_agent,
        tool_name_override="refunding",
        is_enabled=can_customer_refund,
        # input_filter=handoff_filters.remove_all_messages,  # remove all messages before handoff
           # is enable false refund agent fully hide 
     
 ) ])

async def main():
    current_user = CurrentUser(is_logged_in=True) # if true user is loging refund agent call otherwise general agent will be called
        
    result = await Runner.run(    
        general_obj,
        input="what is weather in karachi.i want to refund my order,details are my order id is 12345 , and i want to refund it,",
        run_config=run_config ,
        context=current_user,  # Providing the current user context
        #if i first ask about tools and allow remove tool  so tool will not removed (agr handoffs nh hora )
        # if i ask to handoff to refund agent, it will remove all tools and handoff to refund agent
    )
    print(result.final_output)
    print("[last agent]:", result.last_agent)

if __name__ == "__main__":
    asyncio.run(main())