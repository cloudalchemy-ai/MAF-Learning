import asyncio
import os

import httpx
from a2a.client import A2ACardResolver
from agent_framework.a2a import A2AAgent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def main():
    """Demonstrates connecting to and communicating with an A2A-compliant agent."""
    # 1. Get A2A agent host from environment.
    a2a_agent_host = os.getenv("A2A_AGENT_HOST")
    if not a2a_agent_host:
        raise ValueError("A2A_AGENT_HOST environment variable is not set")

    print(f"Connecting to A2A agent at: {a2a_agent_host}")

    # 2. Resolve the agent card to discover capabilities.
    async with httpx.AsyncClient(timeout=60.0) as http_client:
        resolver = A2ACardResolver(httpx_client=http_client, base_url=a2a_agent_host)
        agent_card = await resolver.get_agent_card()
        print(f"Found agent: {agent_card.name} - {agent_card.description}")

    # 3. Create A2A agent instance.
    async with A2AAgent(
        name=agent_card.name,
        description=agent_card.description,
        agent_card=agent_card,
        url=a2a_agent_host,
    ) as agent:
        # 4. Simple request/response — the agent waits for completion internally.
        #    Even if the remote agent takes a while, background=False (the default)
        #    means the call blocks until a terminal state is reached.
        print("\n--- Non-streaming response ---")
        user_prompt = input("\nWhat is your product idea? ")

        # Send message to A2A agent
        print("\nSending message to A2A agent...")
        response = await agent.run(user_prompt)
        print("Agent Response:")
        for message in response.messages:
            print(f"  {message.text}")

if __name__ == "__main__":
    asyncio.run(main())
