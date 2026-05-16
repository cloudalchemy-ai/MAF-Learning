import asyncio
from collections import defaultdict
from typing import cast

from agent_framework import Message, Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import ConcurrentBuilder
from dotenv import load_dotenv

load_dotenv()

PROMPT = "Plan a trip to Paris."

MAX_OUTPUT_RULE = (
    "\nKeep your response short.\n"
    "- Only 2 bullet points\n"
    "- Maximum 8 words per bullet\n"
    "- No extra explanation\n"
)


def print_agent_block(agent_name: str, text: str) -> None:
    print("\n" + "=" * 60)
    print(f"{agent_name}")
    print("=" * 60)
    print(text.strip())
    print("=" * 60)


def print_final_report(agent_outputs: dict[str, list[str]]) -> None:
    sections = {
        "Food & Dining": "FoodExpert",
        "Accommodation": "AccommodationExpert",
        "Activities": "ActivitiesExpert",
        "Transport": "TransportExpert",
        "Budget": "BudgetExpert",
    }

    print("\n\n" + "#" * 60)
    print("FINAL PARIS TRAVEL REPORT")
    print("#" * 60)

    for section_title, agent_name in sections.items():
        text = "\n".join(agent_outputs.get(agent_name, [])).strip()

        if not text:
            continue

        print(f"\n{section_title}")
        print("-" * 60)
        print(text)

    print("\nReport generated from concurrent agent outputs.")


async def main() -> None:
    client = OpenAIChatClient()

    food_agent = Agent(
        client=client,
        name="FoodExpert",
        instructions="You are a food expert. Suggest local food options." + MAX_OUTPUT_RULE,
    )

    accommodation_agent = Agent(
        client=client,
        name="AccommodationExpert",
        instructions="You are an accommodation expert. Suggest places to stay." + MAX_OUTPUT_RULE,
    )

    activities_agent = Agent(
        client=client,
        name="ActivitiesExpert",
        instructions="You are an activities expert. Suggest things to do." + MAX_OUTPUT_RULE,
    )

    transport_agent = Agent(
        client=client,
        name="TransportExpert",
        instructions="You are a transport expert. Suggest how to travel." + MAX_OUTPUT_RULE,
    )

    budget_agent = Agent(
        client=client,
        name="BudgetExpert",
        instructions="You are a budget expert. Suggest cost tips." + MAX_OUTPUT_RULE,
    )

    workflow = ConcurrentBuilder(
        participants=[
            food_agent,
            accommodation_agent,
            activities_agent,
            transport_agent,
            budget_agent,
        ]
    ).build()

    print("\nStarting Concurrent Workflow")
    print(f"Prompt: {PROMPT}")
    print("-" * 60)

    agent_outputs: dict[str, list[str]] = defaultdict(list)

    async for event in workflow.run(PROMPT, stream=True):
        if event.type == "output":
            messages = cast(list[Message], event.data)

            for message in messages:
                if not message.text:
                    continue

                agent_name = message.author_name or "UnknownAgent"

                if agent_name == "user":
                    continue

                agent_outputs[agent_name].append(message.text)

    if not agent_outputs:
        print("No agent output received.")
        return

    print("\nINDIVIDUAL AGENT OUTPUTS")

    for agent_name in [
        "FoodExpert",
        "AccommodationExpert",
        "ActivitiesExpert",
        "TransportExpert",
        "BudgetExpert",
    ]:
        if agent_name in agent_outputs:
            text = "\n".join(agent_outputs[agent_name])
            print_agent_block(agent_name, text)

    print_final_report(agent_outputs)


if __name__ == "__main__":
    asyncio.run(main())