"""
Incident Triage Agent with Observability
Microsoft Agent Framework 1.0+ | OpenAIChatClient

Alert → agent calls lookup_runbook → triage summary.
Observability: span tree, token usage, model, latency.

.env:  OPENAI_API_KEY=sk-...   OPENAI_CHAT_MODEL=gpt-4o-mini
pip install agent-framework python-dotenv opentelemetry-sdk
"""

import asyncio, os, time
from typing import Annotated
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
os.environ["ENABLE_INSTRUMENTATION"] = "true"
os.environ["ENABLE_SENSITIVE_DATA"] = "true"

import warnings
warnings.filterwarnings("ignore", message=".*experimental.*", category=Warning)

# ── OpenTelemetry setup ──────────────────────────────────────────────
from opentelemetry import trace as otel
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import SpanKind, StatusCode
from opentelemetry.trace.span import format_trace_id, format_span_id

captured_spans: list = []


class ListExporter(SpanExporter):
    """Collects finished spans into a list for post-run reporting."""
    def export(self, spans) -> SpanExportResult:
        captured_spans.extend(spans)
        return SpanExportResult.SUCCESS
    def shutdown(self): ...


provider = TracerProvider(resource=Resource.create({"service.name": "triage"}))
provider.add_span_processor(SimpleSpanProcessor(ListExporter()))
otel.set_tracer_provider(provider)

from agent_framework.observability import enable_instrumentation
enable_instrumentation(enable_sensitive_data=True)

tracer = otel.get_tracer("triage")

# ── Agent + Tool ─────────────────────────────────────────────────────
from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatClient
from pydantic import Field

RUNBOOK = """Owner: payments-team | Escalation: L2 → payments-oncall
Known issues:
  - Connection pool exhaustion >500 TPS — restart pods, check HPA
  - TLS cert expiry causes 503s — verify cert-manager
  - DB replica lag >5s triggers timeouts — check RDS replication
Diagnostics: kubectl logs -l app=payment-gateway -n payments --tail=200"""


@tool(approval_mode="never_require")
async def lookup_runbook(
    service_name: Annotated[str, Field(description="Name of the failing service")],
) -> str:
    """Look up the operational runbook for a service."""
    await asyncio.sleep(0.3)  # simulate I/O
    return RUNBOOK if "payment" in service_name.lower() else f"No runbook for '{service_name}'."


# ── Observability report ─────────────────────────────────────────────
def print_observability(trace_id: str, elapsed: float):
    SEP = "=" * 66

    # Build parent lookup for depth calculation
    span_ids = {format_span_id(s.context.span_id) for s in captured_spans}

    def depth(s):
        d, cur = 0, s
        while cur.parent and format_span_id(cur.parent.span_id) in span_ids:
            d += 1
            cur = next((p for p in captured_spans
                        if format_span_id(p.context.span_id) == format_span_id(cur.parent.span_id)), cur)
            if cur == s: break
        return d

    def tag(name):
        if "invoke_agent" in name: return "AGENT"
        if "execute_tool" in name: return "TOOL"
        if "chat" in name:        return "LLM"
        return "ROOT"

    print(f"\n{SEP}")
    print(f"  OBSERVABILITY  —  trace {trace_id}")
    print(f"{SEP}\n")
    print(f"  Span Tree ({len(captured_spans)} spans):\n")

    for s in captured_spans:
        ms = (s.end_time - s.start_time) / 1e6
        indent = "   " * depth(s)
        bar = "#" * max(1, int(ms / 100))
        print(f"    {indent}[{tag(s.name):>5}] {s.name:<36} {ms:>6.0f}ms  {bar}")

    # Aggregate token usage + model
    tok_in = tok_out = 0
    model = ""
    for s in captured_spans:
        a = s.attributes or {}
        tok_in  += a.get("gen_ai.usage.input_tokens", 0)
        tok_out += a.get("gen_ai.usage.output_tokens", 0)
        model    = a.get("gen_ai.request.model", "") or model

    print(f"\n  Tokens  : {tok_in} in / {tok_out} out / {tok_in + tok_out} total")
    print(f"  Model   : {model or 'n/a'}")
    print(f"  Latency : {elapsed:.2f}s\n{SEP}\n")


# ── Main ─────────────────────────────────────────────────────────────
async def main():
    agent = Agent(
        client=OpenAIChatClient(),
        name="TriageAgent",
        instructions=(
            "You are an L1 triage agent. Use lookup_runbook to get the "
            "runbook, then provide a short triage: severity, probable cause, "
            "and next steps. Be concise."
        ),
        tools=lookup_runbook,
        id="triage-agent",
    )

    alert = (
        "[ALERT] P2 — payment-gateway — Error rate 23% (threshold 5%) — "
        "HTTP 503 spike — eu-west-1 — PagerDuty INC-40291"
    )

    with tracer.start_as_current_span("Triage Incident", kind=SpanKind.CLIENT) as root:
        trace_id = format_trace_id(root.get_span_context().trace_id)
        t0 = time.perf_counter()

        print(f"\n{'=' * 66}\n  INCIDENT TRIAGE AGENT\n{'=' * 66}\n  Alert: {alert}\n")
        print("  TriageAgent: ", end="", flush=True)

        async for chunk in agent.run(alert, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)

        elapsed = time.perf_counter() - t0
        root.set_status(StatusCode.OK)
        print("\n")

    provider.force_flush()
    print_observability(trace_id, elapsed)


if __name__ == "__main__":
    asyncio.run(main())