# Showcase of middleware for security filtering in Azure OpenAI agent
# 1. Read user input
# 2. Middleware checks for banned words
# 3. If banned words found, raise error and block request
# 4. Otherwise, process input and return response

import asyncio
from agent_framework.openai import OpenAIChatClient
from agent_framework import AgentMiddleware
from dotenv import load_dotenv

load_dotenv()


class SecurityMiddleware(AgentMiddleware):
    def __init__(self):
        super().__init__()
        self.current_input = ""

    async def process(self, context, call_next):
        # Check for banned words
        banned_words = ["hack", "password", "secret"]
        if any(word in self.current_input.lower() for word in banned_words):
            raise ValueError("Request blocked: sensitive content detected")

        print(f"[SECURITY] Input: {self.current_input}")

        # Process and return result
        result = await call_next(context)
        print(f"[SECURITY] Response sent")
        return result


async def main():
    client = OpenAIChatClient()

    security = SecurityMiddleware()

    agent = client.as_agent(
        name="secure-agent",
        instructions="You are a helpful assistant.",
        middleware=[security]
    )

    try:
        user_input = input("Enter your prompt: ")
        security.current_input = user_input
        result = await agent.run(user_input)
        print(f"\nResponse: {getattr(result, 'text', str(result))}")
    except ValueError as e:
        print(f"\n {e}")


if __name__ == "__main__":
    asyncio.run(main())