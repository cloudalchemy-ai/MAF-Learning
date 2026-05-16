# Created a simple agent using Azure AI Client for Azure AI Foundry from MAF to respond to queries.
import asyncio
from agent_framework import Agent, Message, Content
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    
    with open("/Users/kshitijjoy_1/Downloads/headshot.png", "rb") as image_file:
        image_data = image_file.read()

    credential = DefaultAzureCredential()

    print(os.getenv("FOUNDRY_PROJECT_ENDPOINT"))
    print(os.getenv("FOUNDRY_MODEL"))


    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model=os.getenv("FOUNDRY_MODEL")
    )

    agent = Agent(
        client=chat_client,
        instructions="You are a helpful assistant",
    )

    message = Message(
        role="user",
        contents=[
            Content.from_data(data=image_data, media_type="image/png"),
            Content.from_text("Describe the image and provide interesting facts")
        ]
    )

    response = await agent.run(message)
    print(response.text)  

if __name__ == "__main__":
    asyncio.run(main())