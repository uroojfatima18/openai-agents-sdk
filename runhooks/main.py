from agents import Agent , RunHooks ,Runner ,RunContextWrapper ,AgentHooks
from typing import TypeVar
from dataclasses import dataclass
from pydantic import BaseModel

class Mytestdata(BaseModel):
    name:str
    age:int

testdata=Mytestdata(name="urooj",age="19")


#runhooks
class MycustomHook(RunHooks):
    def on_agent_start(self, context: RunContextWrapper[Mytestdata], agent: Agent):
        return(f"starting run of the agent:{agent.name},{context.context.name},{context.context.age}")
    
    def on_agent_end(self, agent, output):
        print(f"run complete for agent{agent.name}output: {output.final_output}")

#agenthook
class MycustomAgentHook(AgentHooks):
    def on_start(self, context: RunContextWrapper[Mytestdata], agent: Agent):
        return(f"starting run of the agent:{agent.name}")
    
    def on_end(self,agent, output):
        print(f"run complete for agent{agent.name}output: {output.final_output}")


myagent=Agent (name="test_agent",instructions="you are a helpfull assistant",hooks= MycustomAgentHook())

output=Runner.run_sync(myagent,input = "hello",context=testdata, hooks=MycustomHook())

#generic -> means type of context
T=TypeVar("T")

@dataclass
class   MyTest[T]():
    id: T
    idsub: T

output  =MyTest[str](id="03636",idsub="urooj")









#agent hook
class MyCustomHook(AgentHooks):
    def on_start(self, context, agent):
        return super().on_start(context, agent)
    
    def on_end(self, context, agent, output):
        return super().on_end(context, agent, output)

