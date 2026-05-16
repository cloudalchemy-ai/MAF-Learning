 # Created a simple agent using Azure AI Client for Azure AI Foundry from MAF to respond to queries.
import asyncio
from agent_framework import Agent , Message , tool
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import DefaultAzureCredential
from random import randint
from dotenv import load_dotenv
import os

load_dotenv()

@tool
async def get_weather(location: str) -> str:
    """Get weather for a location.
    
    Args:
        location: The city or location name to get weather for
        
    Returns:
        A string describing the current weather conditions
    """
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


async def main():
    async with DefaultAzureCredential() as credential:
        chat_client = FoundryChatClient(
            credential=credential,
            project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
            model=os.getenv("FOUNDRY_MODEL"),

)
        agent = Agent(
            client=chat_client,
            name="simple-azai-claude-agent-tools",
            description="An agent that demonstrates Azure AI integration with MAF & tools.",
            instructions="You are a helpful assistant that uses Azure AI to respond to queries.",
            tools=[get_weather]
        )

        #Use Message Class to send a message to the agent with additional metadata

        response = await agent.run(Message(role="user", contents=["Give me weather in London"]))
        print(response.text)


if __name__ == "__main__":
        asyncio.run(main())
