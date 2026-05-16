import logging
import os
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent import create_conceptualizer_agent 
from dotenv import load_dotenv
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agent_executor import ProductConceptualizerAgentExecutor
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""
    pass


def main():
    """Starts the Product Conceptualizer Agent server."""
    host = "0.0.0.0" # Use 0.0.0.0 to make it accessible from other machines/docker containers
    port = 10001 # This is the port your HostAgent expects for the Conceptualizer

    try:
        # Check for API key for Google Generative AI (Gemini)
        # Assuming you're using google-generativeai client for tools or the agent itself
        if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
            raise MissingAPIKeyError(
                "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE. "
                "One is required for LLM interaction."
            )

        # --- Define the AgentCard for the Product Conceptualizer Agent ---
        # This card tells other agents (like your HostAgent) what this agent is about.
        capabilities = AgentCapabilities(streaming=True)
        # Define skills relevant to product conceptualization
        skill_conceptualize = AgentSkill(
            id="generate_product_concepts", # Matches the tool name in conceptualizer_agent.py
            name="Generate Product Concepts",
            description="Generates new product ideas based on product type, target audience, and constraints.",
            tags=["product_development", "innovation", "conceptualization"],
            examples=["Generate a product idea for a smart home device.", "I need 3 concepts for sustainable packaging."],
        )
        # Add more skills if your conceptualizer has other distinct tools
        # skill_market_research = AgentSkill(...)

        agent_card = AgentCard(
            name="product_conceptualizer", # IMPORTANT: This MUST match the name HostAgent tries to connect to
            description="An agent that specializes in generating innovative product concepts and ideas.",
            url=f"http://localhost:10001", # URL where this agent will be accessible
            version="1.0.0",
            defaultInputModes=["text/plain"],
            defaultOutputModes=["text/plain", "application/json"], # Can output text or structured JSON
            capabilities=capabilities,
            skills=[skill_conceptualize], # List all relevant skills here
        )

        # --- Initialize the Google ADK Agent ---
        # This imports the agent definition (with its instruction and tools)
        adk_agent = create_conceptualizer_agent() # Calls a function from conceptualizer_agent.py

        # --- Set up the ADK Runner ---
        # The runner manages the agent's execution, memory, and sessions
        runner = Runner(
            app_name=agent_card.name,
            agent=adk_agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
        agent_executor = ProductConceptualizerAgentExecutor(runner)

        # --- Set up the A2A Request Handler and Server ---
        # DefaultRequestHandler takes the ADK Runner to process incoming A2A messages
        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor, # DefaultRequestHandler expects a Runner as agent_executor
            task_store=InMemoryTaskStore(), # Stores task states (e.g., PENDING, COMPLETED)
        )
        # A2AStarletteApplication wraps the handler to create a web application
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        logger.info(f"Starting Product Conceptualizer Agent server on {host}:{port}...")
        uvicorn.run(server.build(), host=host, port=port) # Starts the Uvicorn web server

    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main()