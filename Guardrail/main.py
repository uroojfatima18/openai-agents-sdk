from agents import Runner , Agent , RunConfig, GuardrailFunctionOutput ,RunContextWrapper,AsyncOpenAI , OpenAIChatCompletionsModel , set_tracing_disabled , input_guardrail , InputGuardrailTripwireTriggered
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model =OpenAIChatCompletionsModel(
    model ="gemini-2.0-flash",
    openai_client=external_client
)

run_config=RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

class Work(BaseModel):
    eng:str

guardrail_agent =   Agent(
    name ="guardrail checker",
    instructions="you are a guardrail checkr ,check student ask eng and urdu realated question or not",
    output_type=Work
)
@input_guardrail
async def english_guardrail(
    ctx:RunContextWrapper ,
    agent =Agent,
    input= str
)->GuardrailFunctionOutput:
    result= await Runner.run(guardrail_agent, input, context=ctx.context ,run_config=run_config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_work_realated_to_eng,
    )
agent=Agent(
    name="student checker",
    instructions="only question about english",
    input_guardrails=[english_guardrail]
)
async def main():
   try:
    await Runner.run(agent , input="write 5 points essay on quaid-e-azam" , run_config=run_config)
    print("Guardrail didn't trip - this is unexpected")
   except InputGuardrailTripwireTriggered:
    print("guardrail triggered")
