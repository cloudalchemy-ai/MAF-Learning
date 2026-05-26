import asyncio
import logging
import os
from random import randint
from typing import Annotated

import dotenv
from pydantic import Field

from agent_framework import Agent, tool
from agent_framework.observability import (
    create_resource,
    enable_instrumentation,
    get_tracer,
)
from agent_framework.openai import OpenAIChatClient
import sys
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential
from azure.monitor.opentelemetry import configure_azure_monitor

from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.trace.span import format_trace_id

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables
dotenv.load_dotenv()

logger = logging.getLogger(__name__)


# -----------------------------
# Tool definition
# -----------------------------
@tool(approval_mode="never_require")
async def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    await asyncio.sleep(randint(0, 10) / 10.0)
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return (
        f"The weather in {location} is "
        f"{conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."
    )


# -----------------------------
# Main application
# -----------------------------
async def main():
    async with (
        AzureCliCredential() as credential,
        AIProjectClient(
            endpoint=os.environ["PROJECT_ENDPOINT"],
            credential=credential,
        ) as project_client,
    ):
        # Get Application Insights connection string from Azure AI Project
        try:
            conn_string = (
                await project_client.telemetry
                .get_application_insights_connection_string()
            )
        except Exception:
            logger.warning(
                "No Application Insights connection string found for the Azure AI Project. "
                "Please ensure Application Insights is configured for this project."
            )
            return

        # Verify connection string is valid
        print(f"📡 App Insights connection: {conn_string[:50]}...")

        # Configure Azure Monitor ONCE
        configure_azure_monitor(
            connection_string=conn_string,
            enable_live_metrics=True,
            resource=create_resource(),
            enable_performance_counters=False,
        )

        # Enable Agent Framework instrumentation
        enable_instrumentation(enable_sensitive_data=True)

        print("✅ Observability is set up. Starting Weather Agent...")

        questions = [
            "What's the weather in Amsterdam?",
            "and in Paris, and which is better?",
            "Why is the sky blue?",
        ]

        with get_tracer().start_as_current_span(
            "Weather Agent Chat",
            kind=SpanKind.CLIENT,
        ) as current_span:
            trace_id = format_trace_id(current_span.get_span_context().trace_id)
            print(f"Trace ID: {trace_id}")

            agent = Agent(
                client=OpenAIChatClient(),
                tools=get_weather,
                name="WeatherAgent",
                instructions="You are a weather assistant.",
                id="weather-agent",
            )

            session = agent.create_session()

            for question in questions:
                print(f"\nUser: {question}")
                print(f"{agent.name}: ", end="")

                async for update in agent.run(
                    question,
                    session=session,
                    stream=True,
                ):
                    if update.text:
                        print(update.text, end="", flush=True)

            print()  # newline after last streamed response

        # --- Flush telemetry before exit ---
        print("\n⏳ Flushing telemetry to Application Insights...")
        provider = trace.get_tracer_provider()
        if hasattr(provider, "force_flush"):
            provider.force_flush(timeout_millis=10000)

        print(f"✅ Done! Look up Trace ID in App Insights → Transaction search:")
        print(f"   {trace_id}")
        print(f"\n   Or run this Kusto query in Logs:")
        print(f'   dependencies | where operation_Id == "{trace_id}" | order by timestamp asc')


if __name__ == "__main__":
    asyncio.run(main())