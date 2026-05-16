import asyncio
from agent_framework import Agent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv()


async def playwright_mcp_news_agent():
    # Create the chat client
    chat_client = OpenAIChatClient()

    # Create the MCP tool — must stay connected for the agent's lifetime
    async with MCPStdioTool(
        name="PlaywrightMCPTool",
        command="npx",
        args=["@playwright/mcp@latest"],
        load_prompts=False,
    ) as mcp_server:

        # Create a ChatAgent with MCP tools passed via tools param
        agent = Agent(
            client=chat_client,
            name="NewsReaderAgent",
            instructions="""
            You are a helpful assistant that reads news websites like a human.
            Navigate pages, open articles, and summarise content clearly.
            Focus on accuracy and clarity and use emojis.
            """,
            tools=mcp_server,
        )

        result = await agent.run(
            """
                1. Go to https://www.bbc.co.uk/sport
                2. Extract the top 3 headline titles.
                4. Summarise each in 1-2 bullet points with one overall trend and use emojis.
            """
    )

        print(result)


asyncio.run(playwright_mcp_news_agent())