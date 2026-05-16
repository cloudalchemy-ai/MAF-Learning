# =============================================================================
# 🧬 AI Science Tutor Agent — Professor Spark (with Short-Term Memory)
# =============================================================================
# A simple but engaging science tutor that REMEMBERS the conversation
# using Agent Framework's built-in Session object for short-term memory.
#
# Built with Agent Framework + OpenAIChatClient
# =============================================================================

import asyncio
from dotenv import load_dotenv
load_dotenv()

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

# -----------------------------------------------------------------------------
# THE TUTOR'S PERSONALITY & TEACHING STYLE
# -----------------------------------------------------------------------------

TUTOR_PROMPT = """
You are Professor Spark ⚡ — a fun, enthusiastic AI science tutor.

HOW YOU TEACH:
- Start every explanation with a surprising hook or "did you know?" fact
- Use simple analogies first, then build up to the real science
- After explaining, always ask a follow-up question to check understanding
- If a student gets something wrong, say "Great thinking! But here's the twist..."

WHAT YOU CAN DO (offer these naturally during conversation):
- 🧪 Experiments: Suggest simple home experiments using household items
- 📝 Quizzes: Offer 3 quick multiple-choice questions to test understanding  
- 🗺️ Roadmaps: Show what to learn next if the student wants to go deeper
- 🎯 Analogies: Explain tough concepts using everyday things (cooking, sports, games)

IMPORTANT RULES:
- Keep responses short and conversational (not essay-length)
- Use emoji sparingly but effectively
- Never just dump information — make it a dialogue
- Adapt your language to the student's level
- When you give a quiz, REMEMBER the questions you asked
- When the student answers a quiz, grade their answers based on the quiz
  you gave them earlier in this conversation — do NOT ask them to repeat
  the questions back to you
- Keep quizzes on the SAME TOPIC you were just discussing
"""

# -----------------------------------------------------------------------------
# INTERACTIVE TUTOR SESSION
# -----------------------------------------------------------------------------

WELCOME = """
╔═══════════════════════════════════════════════════╗
║  🧬  Professor Spark's Science Lab  ⚡            ║
╠═══════════════════════════════════════════════════╣
║                                                   ║
║  Try:                                             ║
║  • "Why is the sky blue?"                         ║
║  • "Explain DNA like I'm 10"                      ║
║  • "Quiz me on the solar system"                  ║
║  • "Suggest an experiment about electricity"      ║
║                                                   ║
║  Type 'quit' to exit                              ║
╚═══════════════════════════════════════════════════╝
"""


async def main() -> None:
    # Create the tutor agent
    tutor = Agent(
        client=OpenAIChatClient(),
        instructions=TUTOR_PROMPT,
        name="ProfessorSpark",
    )

    # Create a Session — this is the short-term memory that keeps
    # track of the entire conversation automatically
    session = tutor.create_session()

    print(WELCOME)

    # Kick off with a mind-blowing science fact
    opening = await tutor.run(
        "Introduce yourself in one sentence and share one mind-blowing science fact.",
        session=session,  # session tracks this exchange
    )
    print(f"\n⚡ Professor Spark: {opening.text}\n")

    # Conversation loop — real back-and-forth tutoring
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("\n⚡ Professor Spark: Keep asking 'why?' — that's how all great science starts! 🚀\n")
            break

        # Pass the same session object — the agent automatically remembers
        # everything said so far (quiz questions, explanations, etc.)
        response = await tutor.run(user_input, session=session)

        print(f"\n⚡ Professor Spark: {response.text}\n")


if __name__ == "__main__":
    asyncio.run(main())