# Create a sample MAF file with OpenAI's API

import asyncio
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv("/Users/kshitijjoy_1/Documents/maf-course-v1/.env")

async def main():
    agent = OpenAIChatClient().as_agent (
        name="Sample MAF OpenAI Agent",
        instructions="You are a helpful assistant that generates MAF files based on user input."
    )

    response= await agent.run("Give me some bullet points for Microsoft Agent Framework in AI")
    print(response.text)

if __name__ == "__main__":
        asyncio.run(main())

        