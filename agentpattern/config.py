from dotenv import load_dotenv ,find_dotenv
load_dotenv(find_dotenv())
from agents import RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client=AsyncOpenAI(
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