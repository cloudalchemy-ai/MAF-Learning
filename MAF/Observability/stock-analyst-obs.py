"""
Stock Analyst Agent with Azure Monitor Observability
Microsoft Agent Framework 1.0+ | OpenAIChatClient

.env:  OPENAI_API_KEY=sk-...   OPENAI_CHAT_MODEL=gpt-4o-mini
       PROJECT_ENDPOINT=https://...
"""

import asyncio
import logging
import os
import sys
from random import uniform, choice
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

from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential
from azure.monitor.opentelemetry import configure_azure_monitor

from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.trace.span import format_trace_id

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dotenv.load_dotenv()
logger = logging.getLogger(__name__)


# ── Tool ──────────────────────────────────────────────────────────────

@tool(approval_mode="never_require")
async def get_stock_price(
    ticker: Annotated[str, Field(description="Stock ticker, e.g. AAPL")],
) -> str:
    """Get the current price and daily change for a stock."""
    await asyncio.sleep(uniform(0.1, 0.4))

    prices = {
        "AAPL": 195, "MSFT": 430, "NVDA": 880,
        "GOOG": 175, "TSLA": 178, "AMZN": 186,
    }
    ticker = ticker.upper().strip()
    base = prices.get(ticker)
    if not base:
        return f"Unknown ticker '{ticker}'. Try: {', '.join(prices)}"

    price = round(base * uniform(0.95, 1.05), 2)
    change = round(uniform(-3, 4), 2)
    rating = choice(["Buy", "Hold", "Sell"])
    return (
        f"{ticker}: ${price} ({'+' if change > 0 else ''}{change}%) "
        f"| Analyst rating: {rating}"
    )


# ── Main ──────────────────────────────────────────────────────────────

async def main():
    async with (
        AzureCliCredential() as credential,
        AIProjectClient(
            endpoint=os.environ["PROJECT_ENDPOINT"],
            credential=credential,
        ) as project_client,
    ):
        try:
            conn_string = (
                await project_client.telemetry
                .get_application_insights_connection_string()
            )
        except Exception:
            logger.warning("No App Insights connection string found.")
            return

        print(f"📡 App Insights: {conn_string[:50]}...")

        configure_azure_monitor(
            connection_string=conn_string,
            enable_live_metrics=True,
            resource=create_resource(),
            enable_performance_counters=False,
        )
        enable_instrumentation(enable_sensitive_data=True)
        print("✅ Starting Stock Analyst Agent...\n")

        questions = [
            "What's the price of NVDA?",
            "Compare AAPL and MSFT — which looks better?",
        ]

        with get_tracer().start_as_current_span(
            "Stock Analyst Chat",
            kind=SpanKind.CLIENT,
        ) as span:
            trace_id = format_trace_id(span.get_span_context().trace_id)
            print(f"Trace ID: {trace_id}\n")

            agent = Agent(
                client=OpenAIChatClient(),
                tools=get_stock_price,
                name="StockAnalyst",
                instructions=(
                    "You are a stock analyst. Use get_stock_price to look up prices. "
                    "Give concise analysis. Remind users this is simulated data."
                ),
                id="stock-analyst",
            )

            session = agent.create_session()

            for question in questions:
                print(f"User: {question}")
                print(f"{agent.name}: ", end="")
                async for update in agent.run(question, session=session, stream=True):
                    if update.text:
                        print(update.text, end="", flush=True)
                print("\n")

        provider = trace.get_tracer_provider()
        if hasattr(provider, "force_flush"):
            provider.force_flush(timeout_millis=10000)

        print(f"✅ Trace ID: {trace_id}")
        print(f'   Kusto: dependencies | where operation_Id == "{trace_id}" | order by timestamp asc')


if __name__ == "__main__":
    asyncio.run(main())