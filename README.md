# Microsoft Agent Framework (MAF): Build Enterprise AI Agents

A hands-on course covering the **Microsoft Agent Framework (MAF)** — from the smallest "hello agent" sample up to real-world multi-agent systems with A2A, MCP, RAG, and human-in-the-loop tooling.

Every module is self-contained: each subfolder is a runnable example with its own `main.py` (or equivalent) and, where useful, its own `Readme.md` and architecture diagram.

---

## Repository layout

```
MAF/
├── MAF Concepts/                      # Bare-minimum MAF building blocks
├── Model & Platform Agnostic/         # Same agent, different model providers
├── Building_basic_agents_with_real_tools/   # Tools, streaming, HITL, middleware
├── Orchestration_workflows/           # Sequential, Concurrent, Handoff patterns
├── Build_real_world_agents/           # End-to-end applications
└── Observability/                     # Tracing, token usage, and latency with OpenTelemetry
```

---

## Modules

### 1. MAF Concepts — [MAF/MAF Concepts/](MAF/MAF%20Concepts/)

The smallest possible MAF programs. Use these to learn the core primitives one at a time.

| File | Concept |
|---|---|
| [sample-maf-claude-AgentClass.py](MAF/MAF%20Concepts/sample-maf-claude-AgentClass.py) | Creating an agent with the `Agent` class |
| [sample-maf-claude-MessaageClass.py](MAF/MAF%20Concepts/sample-maf-claude-MessaageClass.py) | Working with the `Message` class |
| [sample-maf-multi-turn.py](MAF/MAF%20Concepts/sample-maf-multi-turn.py) | Multi-turn conversations and sessions |
| [sample-maf-tool-deco.py](MAF/MAF%20Concepts/sample-maf-tool-deco.py) | Defining tools with the `@tool` decorator |
| [sample-maf-mcp.py](MAF/MAF%20Concepts/sample-maf-mcp.py) | Connecting an agent to an MCP server |
| [sample-maf-a2a.py](MAF/MAF%20Concepts/sample-maf-a2a.py) | Agent-to-agent (A2A) communication |

### 2. Model & Platform Agnostic — [MAF/Model & Platform Agnostic/](MAF/Model%20&%20Platform%20Agnostic/)

The same MAF agent running against three different chat backends — demonstrates that MAF is provider-agnostic.

| File | Backend |
|---|---|
| [sample-maf-openai.py](MAF/Model%20&%20Platform%20Agnostic/sample-maf-openai.py) | OpenAI |
| [sample-maf-azopenai.py](MAF/Model%20&%20Platform%20Agnostic/sample-maf-azopenai.py) | Azure OpenAI |
| [sample-maf-claude.py](MAF/Model%20&%20Platform%20Agnostic/sample-maf-claude.py) | Anthropic Claude |

### 3. Building basic agents with real tools — [MAF/Building_basic_agents_with_real_tools/](MAF/Building_basic_agents_with_real_tools/)

Layered on top of the concepts module, these scripts wire agents up to features you'd actually ship.

| File | Feature |
|---|---|
| [maf-tool-calling-hitl.py](MAF/Building_basic_agents_with_real_tools/maf-tool-calling-hitl.py) | Tool calling with human-in-the-loop approval (`approval_mode="always_require"`) |
| [maf-claude-streaming.py](MAF/Building_basic_agents_with_real_tools/maf-claude-streaming.py) | Token-level response streaming |
| [maf-middleware.py](MAF/Building_basic_agents_with_real_tools/maf-middleware.py) | Custom middleware around agent calls |
| [analyze-images.py](MAF/Building_basic_agents_with_real_tools/analyze-images.py) | Multimodal input — sending images to the agent |

### 4. Orchestration workflows — [MAF/Orchestration_workflows/](MAF/Orchestration_workflows/)

Three canonical multi-agent orchestration patterns built with `WorkflowBuilder`.

| Pattern | Folder | Use case |
|---|---|---|
| **Sequential** | [Sequential_orchestration/](MAF/Orchestration_workflows/Sequential_orchestration/) | Analyzer → Optimizer → Reviewer pipeline (social media post optimizer) |
| **Concurrent** | [Concurrent_orchestration/](MAF/Orchestration_workflows/Concurrent_orchestration/) | Fan-out work to multiple agents in parallel, then aggregate |
| **Handoff** | [Handoff_orchestration/](MAF/Orchestration_workflows/Handoff_orchestration/) | One agent delegates control to another based on context |

Each subfolder includes an architecture diagram and a `Readme.md` walking through the pattern.

### 5. Observability — [MAF/Observability/](MAF/Observability/)

Instrument agents with [OpenTelemetry](https://opentelemetry.io/) to see exactly what they do at runtime: the span tree (agent → tool → LLM calls), token usage, model name, and end-to-end latency. MAF emits standard [GenAI semantic-convention](https://opentelemetry.io/docs/specs/semconv/gen-ai/) traces, so the same instrumentation works whether you export to a local console or to a hosted backend.

Two export targets are demonstrated:

| File | Backend | What it shows |
|---|---|---|
| [inc-triage-obs.py](MAF/Observability/inc-triage-obs.py) | **Local / console** — custom `SpanExporter` collects finished spans | Incident-triage agent calls `lookup_runbook`, then prints a span tree with per-span latency bars, aggregated token counts, and the model used — no cloud account required |
| [stock-analyst-obs.py](MAF/Observability/stock-analyst-obs.py) | **Azure Monitor / Application Insights** | Stock-analyst agent exports traces to App Insights via `configure_azure_monitor`; prints a Trace ID and a ready-to-run Kusto query for Transaction search |

The core pattern across all three:

```python
from agent_framework.observability import enable_instrumentation, get_tracer

enable_instrumentation(enable_sensitive_data=True)   # turn on MAF's GenAI tracing

with get_tracer().start_as_current_span("My Agent Chat", kind=SpanKind.CLIENT) as span:
    trace_id = format_trace_id(span.get_span_context().trace_id)
    # ... run the agent; every agent/tool/LLM call nests under this root span
```

- **Local first**: run `inc-triage-obs.py` to understand the span model with zero setup — it only needs `OPENAI_API_KEY` and the OpenTelemetry SDK.
- **Then go cloud**: the Azure samples need an Azure AI Project with Application Insights enabled (set `PROJECT_ENDPOINT`) and a logged-in Azure CLI (`az login`) for `AzureCliCredential`.

Architecture diagrams (`inc-triage-agent-flow.png`, `stock-analyst-agent-flow.png`) live alongside the code.

### 6. Build real-world agents — [MAF/Build_real_world_agents/](MAF/Build_real_world_agents/)

Full applications combining the concepts above.

| Project | What it does |
|---|---|
| [AI_Science_tutor/](MAF/Build_real_world_agents/AI_Science_tutor/) | Conversational science tutor ("Professor Spark") with session memory, quizzes, and analogies |
| [Playwright_MCP/](MAF/Build_real_world_agents/Playwright_MCP/) | Agent that drives a real browser via the Playwright MCP server |
| [Doc-Insights/](MAF/Build_real_world_agents/Doc-Insights/) | RAG over local documents (`maf-rag.py` + a sample `company_policy.md`) |
| [Idea_generator_and_validator/](MAF/Build_real_world_agents/Idea_generator_and_validator/) | A2A: a local MAF agent calls a remote agent that generates and validates startup ideas |
| [Product_conceptualizer/](MAF/Build_real_world_agents/Product_conceptualizer/) | A2A: turns a rough product idea into a structured concept brief |
| [Study_schedule_agent_ADK/](MAF/Build_real_world_agents/Study_schedule_agent_ADK/) | A2A between MAF and a Google ADK remote agent that builds personalised study plans |

---

## Getting started

### 1. Clone

```bash
git clone https://github.com/cloudalchemy-ai/MAF-Learning.git
cd MAF-Learning
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows
```

### 3. Install dependencies

Most modules ship their own `requirements.txt`. Install per-project:

```bash
pip install -r MAF/Build_real_world_agents/AI_Science_tutor/requirements.txt
```

The common baseline across all modules is:

```
agent-framework
python-dotenv
openai
```

Provider-specific modules additionally need `azure-identity`, `anthropic`, `playwright`, `a2a-sdk`, or `google-adk` depending on the example. The Observability module needs `opentelemetry-sdk` (local sample) and `azure-monitor-opentelemetry` + `azure-ai-projects` (Azure samples).

### 4. Configure secrets

Create a `.env` file at the repo root. Each module reads only the variables it needs:

```env
# OpenAI
OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4o-mini

# Azure OpenAI / Foundry
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=
FOUNDRY_PROJECT_ENDPOINT=
FOUNDRY_MODEL=

# Anthropic
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-sonnet-4-5

# Google (for the ADK remote agent example)
GOOGLE_API_KEY=

# Observability (Azure App Insights sample — stock-analyst-obs.py)
PROJECT_ENDPOINT=          # Azure AI Project endpoint with Application Insights enabled
```

> The local observability sample (`inc-triage-obs.py`) needs no Azure config — it sets `ENABLE_INSTRUMENTATION` / `ENABLE_SENSITIVE_DATA` in-process and exports spans to the console.

`.env` is gitignored — never commit it.

### 5. Run an example

```bash
python "MAF/MAF Concepts/sample-maf-tool-deco.py"
```

---

## Suggested learning path

1. **MAF Concepts** — get comfortable with `Agent`, `Message`, tools, sessions
2. **Model & Platform Agnostic** — swap providers without changing agent logic
3. **Building basic agents with real tools** — add streaming, HITL, middleware
4. **Orchestration workflows** — compose multiple agents
5. **Observability** — trace, measure, and debug agents with OpenTelemetry (local first, then Azure App Insights)
6. **Build real-world agents** — A2A, MCP, and RAG in production-shaped projects

---

## Notes

- Folder names use a mix of spaces and underscores — quote paths in the shell where needed.
- The A2A examples (`Idea_generator_and_validator`, `Product_conceptualizer`, `Study_schedule_agent_ADK`) run a remote agent as a separate process; see each project's `Readme.md` for the two-terminal startup sequence.
- Architecture diagrams (`*.png`, `*.jpg`) live next to the code they describe.
