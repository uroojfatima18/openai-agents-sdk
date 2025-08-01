from config import run_config
import asyncio
from pydantic import BaseModel, Field, field_validator
from agents import function_tool,Agent, Runner
from typing import Optional


# question: How to use Pydantic's field_validator?
@function_tool(is_enabled=True)
async def add_numbers(a: int, b: int) -> int:
    return a + b

@function_tool(is_enabled=True)
async def multiply_numbers(a: int, b: int) -> int:
    return a * b
agent=Agent(
    name="add and multiply",
    instructions="You add two numbers together.",
    tools=[add_numbers, multiply_numbers],

)
result=Runner.run_sync(
    agent, 
    "What is 2 + 3 and 4 * 5?",
    run_config=run_config
              )  

print(f"result:{result.final_output}")


# question: How to use Pydantic's model_dump with exclude_unset?
class Profile(BaseModel):
    name: str
    age: Optional[int] = None
    city: Optional[str] = None

p = Profile(name="Urooj", city="Lahore")
print("Default dump:", p.model_dump())
print("Exclude unset:", p.model_dump(exclude_unset=True))


# question: How to use computed fields in Pydantic?
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

r = Rectangle(width=5, height=10)
print("Area:", r.area)
print("Dump:", r.model_dump())
