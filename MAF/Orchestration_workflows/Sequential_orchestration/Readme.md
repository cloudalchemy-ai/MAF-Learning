# Social Media Post Optimizer

A sequential multi-agent pipeline that transforms raw social media posts into high-engagement content using Microsoft Agent Framework 1.0+ and OpenAI.

## Pipeline overview

```
┌────────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  User post  │────▶│  Analyzer   │────▶│  Optimizer    │────▶│  Reviewer   │
│  (raw text) │     │  (tone/gaps)│     │  (rewrite)    │     │  (polish)   │
└────────────┘     └─────────────┘     └──────────────┘     └─────────────┘
                                                                    │
                                                                    ▼
                                                            ┌──────────────┐
                                                            │ Optimized    │
                                                            │ post output  │
                                                            └──────────────┘
```

## How it works

Three specialised AI agents process the post in sequence, each building on the previous agent's output:

1. **AnalyzerAgent** — Examines tone, identifies engagement gaps, and produces one key recommendation. Output is a concise 3-sentence analysis.

2. **OptimizerAgent** — Rewrites the post with improved engagement hooks, relevant hashtags, emojis, and a call-to-action. Outputs only the new post.

3. **ReviewerAgent** — Polishes grammar, validates hashtag relevance, and rebalances emoji usage. Outputs the final publication-ready post.


## Key concepts

| Concept | Description |
|---|---|
| `OpenAIChatClient` | Wrapper around the OpenAI chat completions API |
| `.as_agent()` | Creates an agent with a name and system instructions |
| `WorkflowBuilder` | Composes agents into a sequential (or branching) DAG |
| `AgentResponseUpdate` | Streaming event carrying the author name and text chunk |
| `stream=True` | Enables token-level streaming through the workflow |

