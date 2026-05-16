"""
This file serves as the main entry point for the application.

It initializes the A2A server, defines the agent's capabilities,
and starts the server to handle incoming requests. Notice the agent runs on port 10011.
"""

import logging

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from .agent import BusinessIdeaAgent                   
from .agent_executor import BusinessIdeaAgentExecutor  
from dotenv import load_dotenv

load_dotenv()

#configure logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=10011)
def main(host, port):
    """Entry point for the A2A Business Idea Agent."""   
    try:
        capabilities = AgentCapabilities(streaming=False)
        skill = AgentSkill(
            id='idea_generator',
            name='Business Idea Generator',
            description='Generate and validate business ideas based on user input.',   
            tags=['generate idea', 'validate idea', 'market trends'],                
            examples=[
                'Generate a business idea for a new fitness app',
                'Generate and validate an idea for an eco-friendly product',
            ],
        )

        #create metadata card describing the agent
        agent_card = AgentCard(
            name='Business Idea Agent',
            description='Generates business ideas via N8N and validates them with CrewAI.',  # ✅ updated description
            url=f'http://localhost:10011/',
            version='1.0.0',
            defaultInputModes=BusinessIdeaAgent.SUPPORTED_CONTENT_TYPES,             # ✅ updated
            defaultOutputModes=BusinessIdeaAgent.SUPPORTED_CONTENT_TYPES,            # ✅ updated
            capabilities=capabilities,
            skills=[skill],
        )

        #create request handler with our custom executor and in memory store.
        request_handler = DefaultRequestHandler(
            agent_executor=BusinessIdeaAgentExecutor(),                              # ✅ updated executor
            task_store=InMemoryTaskStore(),
        )

        #initialize A2A server application
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        #start the server using Uvicorn
        import uvicorn

        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        #log startup errors and exit
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()
