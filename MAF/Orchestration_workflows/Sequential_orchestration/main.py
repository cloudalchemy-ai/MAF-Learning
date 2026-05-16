"""
Social Media Post Optimizer — Sequential Multi-Agent Workflow
Uses Microsoft Agent Framework 1.0+ with OpenAIChatClient (direct OpenAI API).
Pipeline: Analyzer → Optimizer → Reviewer

Prerequisites:
    pip install agent-framework python-dotenv
Env vars: OPENAI_API_KEY, OPENAI_CHAT_MODEL (e.g. gpt-4o-mini)
"""

import asyncio

from agent_framework import AgentResponseUpdate, WorkflowBuilder
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PROMPT = (
    "Just finished my morning workout. Feeling good about staying consistent "
    "with my fitness routine. It's been 3 weeks now and I can see some progress. "
    "Anyone else trying to stay motivated?"
)


async def main() -> None:

    client = OpenAIChatClient()

    analyzer = client.as_agent(
        name="AnalyzerAgent",
        instructions=(
            "You are a social media analyst. "
            "Given a post, provide a 3-sentence analysis covering tone, "
            "engagement gaps, and one key recommendation. Be very concise."
        ),
    )

    optimizer = client.as_agent(
        name="OptimizerAgent",
        instructions=(
            "You are a social media optimizer. "
            "Rewrite the post with better engagement, hashtags, emojis, "
            "and a call-to-action. Output only the new post, nothing else."
        ),
    )

    reviewer = client.as_agent(
        name="ReviewerAgent",
        instructions=(
            "You are a social media reviewer. "
            "Polish the post for grammar, hashtag relevance, and emoji balance. "
            "Output only the final post, nothing else."
        ),
    )

    workflow = (
        WorkflowBuilder(start_executor=analyzer)
        .add_edge(analyzer, optimizer)
        .add_edge(optimizer, reviewer)
        .build()
    )

    print("\n===== Agent Framework — Sequential Workflow (OpenAI) =====\n")

    last_author: str | None = None

    async for event in workflow.run(PROMPT, stream=True):
        if event.type == "output" and isinstance(event.data, AgentResponseUpdate):
            update = event.data
            author = update.author_name
            if author != last_author:
                if last_author is not None:
                    print("\n")
                print(f"[{author}]: {update.text}", end="", flush=True)
                last_author = author
            else:
                print(update.text, end="", flush=True)

    print()


if __name__ == "__main__":
    asyncio.run(main())