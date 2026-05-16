# Sample Code to show how to use the Azure MCP tool with MAF. 
# This agent will start an Azure MCP server as a subprocess and use it 
# to answer questions about the user's Azure subscription and resources.

import asyncio , os
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
load_dotenv()


async def main():
    from agent_framework import Agent, MCPStdioTool
    from agent_framework.foundry import FoundryChatClient
    from azure.identity.aio import DefaultAzureCredential

    async with DefaultAzureCredential() as credential:
        client = FoundryChatClient(credential=credential,
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model=os.getenv("FOUNDRY_MODEL"),)

        azure_mcp = MCPStdioTool(
            name="Azure MCP Server",
            command="npx",
            args=["-y", "@azure/mcp@latest", "server", "start"],
            load_prompts=False,
        )

        async with (
            azure_mcp,
            Agent(
                client=client,
                name="AzureOpsAgent",
                instructions=(
                    "You are an Azure operations assistant. "
                    "Use the Azure MCP tools to answer questions about "
                    "the user's Azure subscription and resources. "
                    "Always show output in a nice table"
                ),
                tools=[azure_mcp],
            ) as agent,
        ):
            result = await agent.run("List all resource groups in my subscription.")
            print(f"Agent: {result}")

            result = await agent.run("What storage accounts exist?")
            print(f"Agent: {result}")



if __name__ == "__main__":
    asyncio.run(main())