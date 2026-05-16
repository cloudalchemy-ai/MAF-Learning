import asyncio
from typing import Annotated
from agent_framework import Agent, Message, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import DefaultAzureCredential
from random import randint
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings("ignore")

load_dotenv()


@tool(approval_mode="always_require")
def get_weather(location: Annotated[str, "The city or location name"]) -> str:
    """Get weather for a location."""
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
            name="simple-azai-agent-hitl",
            description="An agent with human-in-the-loop tool approval.",
            instructions="You are a helpful assistant which generates 1 page weather report with emojis",
            tools=[get_weather],
        )

        session = agent.create_session()

        user_input = input("Enter your prompt: ")
        result = await agent.run(user_input, session=session)

        # Handle approval loop
        while result.user_input_requests:
            for request in result.user_input_requests:
                print(f"\n🔔 Approval needed for: {request.function_call.name}")
                print(f"   Arguments: {request.function_call.arguments}")
                approval = input("   Approve? (y/n): ").strip().lower() == "y"

                # Create the approval response
                approval_response = request.to_function_approval_response(approved=approval)

                # Send approval back to the agent with the same session
                result = await agent.run(approval_response, session=session)

        print(f"\nResponse: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())