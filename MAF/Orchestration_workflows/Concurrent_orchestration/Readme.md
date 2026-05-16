# Concurrent Orchestration — Travel Planner

A multi-agent travel planning system built with the Agent Framework. Five specialist agents run **concurrently** to generate a comprehensive travel plan from a single user prompt.

## Architecture

```
                    ┌──────────────┐
                    │  User Prompt │
                    └──────┬───────┘
                           │
                ┌──────────▼──────────┐
                │  ConcurrentBuilder  │
                │  (parallel fan-out) │
                └──┬──┬──┬──┬──┬─────┘
                   │  │  │  │  │
       ┌───────────┘  │  │  │  └───────────┐
       │     ┌────────┘  │  └────────┐     │
       ▼     ▼           ▼           ▼     ▼
  ┌────────┐┌──────────┐┌──────────┐┌────────┐┌────────┐
  │  Food  ││ Accomm.  ││Activities││Transport││ Budget │
  │ Expert ││  Expert  ││  Expert  ││ Expert  ││ Expert │
  └───┬────┘└────┬─────┘└────┬─────┘└───┬────┘└───┬────┘
      │          │           │          │         │
      └──────────┴─────┬─────┴──────────┴─────────┘
                       ▼
          ┌────────────────────────┐
          │  OpenAI Chat API      │
          └────────────┬───────────┘
                       ▼
          ┌────────────────────────┐
          │  Output Collector      │
          │  (stream → print)     │
          └────────────────────────┘
```

## How It Works

The system uses `ConcurrentBuilder` from the Agent Framework to fan out a single prompt to all five agents simultaneously. Each agent calls the OpenAI Chat Completions API independently, and their responses stream back as events. The output collector gathers all results and prints them grouped by agent.

### Agents

| Agent | Role | What it covers |
|-------|------|----------------|
| **FoodExpert** | Culinary & dining | Local dishes, restaurant tiers, street food, dining etiquette |
| **AccommodationExpert** | Hotels & lodging | Budget to luxury options, price ranges, location tips, booking advice |
| **ActivitiesExpert** | Attractions & experiences | Landmarks, local experiences, seasonal activities, day trips |
| **TransportExpert** | Transportation & logistics | Getting there, local transit, cost estimates, navigation tips |
| **BudgetExpert** | Cost & savings | Daily budgets, money-saving tips, affordable alternatives, best travel times |

### Key Design Decisions

**Concurrent, not sequential.** All agents run in parallel, so total latency is roughly the time of the slowest single agent — not the sum of all five.

**Streaming output.** The workflow uses `stream=True` and collects `output` events as they arrive, so results can be displayed progressively.

**Shared client.** All agents share one `OpenAIChatClient` instance, keeping connection overhead low.

**No inter-agent communication.** Each agent operates independently on the same prompt. This is a fan-out pattern, not a pipeline — agents don't see each other's outputs.

