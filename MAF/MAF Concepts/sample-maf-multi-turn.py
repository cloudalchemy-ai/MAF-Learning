# Created a simple agent using Azure AI Client to showcase Short Term Memory.
import asyncio
from agent_framework import Agent , Message
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    credential = DefaultAzureCredential()
    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
            model=os.getenv("FOUNDRY_MODEL"),

)
    agent = Agent(
            client=chat_client,
            name="simple-azai-claude-agent",
         )

        
    agent_session=agent.create_session()

    response1 = await agent.run(Message(role="user", contents=["Give me the bullet points for Microsoft Agent Framework in AI"]),session=agent_session)
    print("---------First Response--------------")
    print("---------------------------------")
    print(response1.text)
    response2 = await agent.run(Message(role="user", contents=["Can you add some emojis to the same response"]),session=agent_session)
    print("---------Second Response--------------")
    print("---------------------------------")
    print(response2.text)


if __name__ == "__main__":
        asyncio.run(main())
