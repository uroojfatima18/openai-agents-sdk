# Dynamic Instructions

from agents import Agent, function_tool,OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI,Runner, RunContextWrapper
from agents.agent import ModelSettings
import agentops
from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
import os
from pydantic import BaseModel
from dataclasses import dataclass

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
    model_provider=external_client
)

@dataclass
class User(BaseModel):
    name:str
    phone:int
    current_conversation:list[str] = []

    def  get_memories(self):
        return f"User{self.name}has phone number{self.phone}"
    
    def update_memory(self, memory:str):
        self.memory = memory
  
    def update_conversation(self, conversation:str):
        self.current_conversation.append(conversation)    
                                         

# function for dynamic instructions
def  get_system_prompt(ctx:RunContextWrapper[User], starting_agent:Agent[User]):
    print("\n[Context]",ctx.context)
    print("\n[Agent]",starting_agent)

    ctx.context.update_memory(f"User {ctx.context.name} has phone number {ctx.context.phone}")
    ctx.context.update_conversation(f"User {ctx.context.name} is asking for help.")
 
    return "your are a helpful agent that can answer user question and help them with their queries"

agent = Agent(
    name="Haiku agent",
    instructions=get_system_prompt
)

user=User(name="Urooj Fatima",phone=1234567890)

result=Runner.run_sync(agent,input="HELLO,?",context=user,run_config=run_config)
print(result.final_output)
print([user.get_memories()])
