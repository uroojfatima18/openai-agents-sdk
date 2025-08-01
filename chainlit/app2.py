#  AI agents with history 100% run code 
import os
import chainlit as cl

from agents import  Agent,RunConfig,OpenAIChatCompletionsModel,set_tracing_disabled, AsyncOpenAI, Runner
from dotenv import load_dotenv ,find_dotenv
from openai.types.responses import ResponseTextDeltaEvent


load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

Model = OpenAIChatCompletionsModel(
    model="gemini-1.5-pro",
    openai_client= provider,
)

run_config =RunConfig(
    model=Model,
    model_provider= provider,
    tracing_disabled=True
)

agent1 =Agent(
    instructions="You are a helpful assistant, you can answer of user questions.",
    name= "Urooj's Support Agent"
) 
@cl.on_chat_start

async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello!, I'm Urooj's made agent.How can i help you?").send()
 
@cl.on_message

async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")


    msg=cl.Message(content="")
    await msg.send()

    history.append({"role": "user","content": message.content})
    result= Runner.run_streamed(
        agent1,
        input= history,
        run_config= run_config,
        )
    async for event in result.stream_events():
       if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
        await  msg.stream_token(event.data.delta)
    

    history.append({"role":"assistant", "content":result.final_output})
    cl.user_session.set("history",history)
   