# Create a sample MAF file with Claude's API and Agent Class

import asyncio
from agent_framework import Agent , Message
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

load_dotenv("/Users/kshitijjoy_1/Documents/maf-course-v1/.env")

async def main():
    credential=DefaultAzureCredential()

    chat_client = FoundryChatClient(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model=os.getenv("FOUNDRY_MODEL"),
        credential=credential,
    )

    agent = Agent(
        client=chat_client,
        name="sample-maf-claude-agent",
        instructions="You are a helpful assistant that generates MAF files based on user input."
    )

    user_message = Message(role="user", contents=["Give me some bullet points for Microsoft Agent Framework in AI"])
    response= await agent.run(user_message)
    print(response.text)

if __name__ == "__main__":
        asyncio.run(main())

        