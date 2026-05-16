"""
🦈 Shark Tank via A2A — Two AI Agents, One Deal
================================================
"""

# ── Standard library ──
import asyncio
import threading
import time

# ── Third-party ──
import uvicorn        # ASGI server that hosts the Founder agent
from dotenv import load_dotenv

# Load .env file so OPENAI_API_KEY is available
load_dotenv()

# Where the Founder agent will listen
FOUNDER_PORT = 9999
FOUNDER_URL = f"http://localhost:{FOUNDER_PORT}"


# ─────────────────────────────────────────────────────────────
# PART 1: The Founder Agent  (runs as an A2A server)
#
# Think of this as a microservice. Other agents can discover it
# via its Agent Card and send it messages over HTTP.
# ─────────────────────────────────────────────────────────────

def start_founder():
    # --- A2A SDK imports (the protocol layer) ---
    from a2a.server.apps import A2AStarletteApplication       # Builds the HTTP app
    from a2a.server.request_handlers import DefaultRequestHandler  # Routes A2A requests
    from a2a.server.tasks import InMemoryTaskStore             # Tracks tasks in memory
    from a2a.types import AgentCapabilities, AgentCard          # Metadata about the agent

    # --- Microsoft Agent Framework imports (the AI layer) ---
    from agent_framework import Agent                          # Core agent class
    from agent_framework.a2a import A2AExecutor                # Bridges MAF Agent ↔ A2A protocol
    from agent_framework.openai import OpenAIChatClient        # OpenAI as the LLM backend

    # 1. Create the AI agent with its personality
    agent = Agent(
        client=OpenAIChatClient(),   # Uses OPENAI_API_KEY from env
        name="Founder Raj",
        instructions=(
            "You are Raj, a hyper-confident startup founder. "
            "When given a theme, invent a startup with: "
            "a catchy name, a one-line elevator pitch, "
            "a business model, and a funding ask (e.g. '$2M seed'). "
            "Be creative and slightly over-the-top. Keep it under 100 words."
        ),
    )

    # 2. Define the Agent Card — this is how other agents discover you
    card = AgentCard(
        name="Founder Raj",
        description="A startup founder who pitches bold ideas.",
        url=f"{FOUNDER_URL}/",
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[],
    )

    # 3. Wire it all together: Agent → A2AExecutor → RequestHandler → App
    handler = DefaultRequestHandler(
        agent_executor=A2AExecutor(agent),   # A2AExecutor adapts the MAF Agent for A2A
        task_store=InMemoryTaskStore(),
    )

    app = A2AStarletteApplication(
        agent_card=card,
        http_handler=handler,
    ).build()   # .build() returns the ASGI app

    # 4. Start serving on port 9999
    uvicorn.run(app, host="0.0.0.0", port=FOUNDER_PORT, log_level="warning")


# ─────────────────────────────────────────────────────────────
# PART 2: The VC Shark Agent  (runs as an A2A client)
#
# This agent doesn't need a server — it just calls the Founder
# over A2A, gets the pitch, and reviews it locally.
# ─────────────────────────────────────────────────────────────

async def run_shark_tank():
    from agent_framework import Agent
    from agent_framework.a2a import A2AAgent           # Wraps a remote A2A agent as a client
    from agent_framework.openai import OpenAIChatClient

    # 1. Create the Shark agent (runs locally, no A2A server needed)
    shark = Agent(
        client=OpenAIChatClient(),
        name="Shark Priya",
        instructions=(
            "You are Priya, a ruthless but fair VC investor. "
            "You will be given a startup pitch. Evaluate it:\n"
            "- Verdict: FUND or PASS\n"
            "- If FUND: state your offer (amount for equity %)\n"
            "- If PASS: state the fatal flaw\n"
            "- End with a witty one-liner\n"
            "Be sharp and dramatic. Keep it under 80 words."
        ),
    )

    # 2. The theme for our pitch round
    themes = [
        "Pitch me a cybersecurity startup",
    ]

    # 3. Connect to the Founder's A2A server
    async with A2AAgent(name="Founder Raj", url=FOUNDER_URL) as founder:

        for i, theme in enumerate(themes, 1):
            print(f"\n{'━' * 55}")
            print(f"  🎬  ROUND {i}")
            print(f"{'━' * 55}")
            print(f"📣  Theme: {theme}\n")

            # Step A — Send the theme to the Founder via A2A
            founder_response = await founder.run(theme)

            # Extract text from the A2A response messages
            pitch = ""
            for msg in founder_response.messages:
                if msg.text:
                    pitch += msg.text
            print(f"🚀  Founder Raj:\n{pitch}\n")

            # Step B — Feed the pitch to the Shark for evaluation
            review = await shark.run(
                f"A founder just pitched you this startup:\n\n{pitch}"
            )
            print(f"🦈  Shark Priya:\n{review}")

    print(f"\n{'━' * 55}")
    print("  🎬  THAT'S A WRAP!")
    print(f"{'━' * 55}\n")


# ─────────────────────────────────────────────────────────────
# PART 3: Main — spin up the Founder server, then run the show
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Start the Founder as a background thread (daemon=True means
    # it dies when the main process exits)
    print(f"🚀 Starting Founder Raj on port {FOUNDER_PORT}...")
    threading.Thread(target=start_founder, daemon=True).start()

    # Give the server a few seconds to start up
    time.sleep(3)
    print("✅ Founder ready! Shark Priya entering the tank...\n")

    # Run the async conversation
    asyncio.run(run_shark_tank())