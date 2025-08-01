from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

async def main():
    llm =ChatGoogleGenerativeAI( 
        model="gemini-2.0-flash",
        google_api_key= os.getenv("GEMINI_API_KEY"),
        )
    
    agent = Agent(    
        task="search from youtube and chrome the highest ranking courses in 2025 ",
        llm=llm,
    )
    await agent.run()

asyncio.run(main())
