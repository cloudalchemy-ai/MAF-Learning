import asyncio
import os
import random
import httpx
from a2a.client import A2ACardResolver
from agent_framework.a2a import A2AAgent
from dotenv import load_dotenv

load_dotenv()


def generate_random_student_calendar():
    """Generate a random weekly student calendar."""
    activities = [
        "Attend class",
        "Study session",
        "Gym workout",
        "Group project",
        "Library reading",
        "Lunch break",
        "Internship work",
        "Relax / Free time",
        "Part-time job",
        "Online course"
    ]

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    calendar = {}

    for day in days:
        # Create a random day schedule (e.g., 3–6 activities)
        num_slots = random.randint(3, 6)
        slots = random.sample(activities, num_slots)
        calendar[day] = slots

    return calendar


async def main():
    """Demonstrates connecting to and communicating with an A2A-compliant agent."""
    # Get A2A agent host from environment
    a2a_agent_host = os.getenv("A2A_AGENT_HOST")
    if not a2a_agent_host:
        raise ValueError("A2A_AGENT_HOST environment variable is not set")

    print(f"Connecting to A2A agent at: {a2a_agent_host}")

    # Initialize A2ACardResolver
    async with httpx.AsyncClient(timeout=60.0) as http_client:
        resolver = A2ACardResolver(httpx_client=http_client, base_url=a2a_agent_host)

        # Get agent card
        agent_card = await resolver.get_agent_card(relative_card_path="/.well-known/agent.json")
        print(f"Found agent: {agent_card.name} - {agent_card.description}")

        # Create A2A agent instance
        agent = A2AAgent(
            name=agent_card.name,
            description=agent_card.description,
            agent_card=agent_card,
            url=a2a_agent_host,
        )

        # Generate random calendar
        calendar = generate_random_student_calendar()
        print("\nGenerated Student Calendar:")
        for day, schedule in calendar.items():
            print(f"{day}: {', '.join(schedule)}")

        # Get live user input
        user_prompt = input("\nFor which subject you want us to create a study schedule? How many hours per day? Learning style? eg: Visual, Auditory, Reading/Writing : ")

        # Combine prompt with calendar
        combined_message = (
            f"Here is a student's weekly calendar:\n{calendar}\n\n"
            f"User question: {user_prompt}"
        )

        # Send message to A2A agent
        print("\nSending message to A2A agent...")
        response = await agent.run(combined_message)

        # Print the response
        print("\nAgent Response:")
        for message in response.messages:
            print(message.text)


if __name__ == "__main__":
    asyncio.run(main())
