import asyncio
from typing import cast

from agent_framework import Message, WorkflowEvent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import HandoffAgentUserRequest, HandoffBuilder
from dotenv import load_dotenv

load_dotenv()

CUSTOMER_PROMPT = "Hi, I need help with my recent order #12345. The product arrived damaged, and I'd like to request a replacement."

SCRIPTED_RESPONSES = [
    "The item arrived damaged. I'd like a replacement shipped to the same address.",
    "Great! Can you confirm the shipping cost won't be charged again?",
    "Thanks for confirming!",
]

AGENTS_CONFIG = {
    "SupportCoordinator": "You are the main customer support coordinator. Greet the customer, understand their issue, and route to the right specialist.",
    "BillingAgent": "You are a billing specialist. Handle invoices, payments, and charges. Route non-billing issues back to SupportCoordinator.",
    "TechnicalAgent": "You are a technical support specialist. Help with technical issues. Route non-technical issues back to SupportCoordinator.",
    "SupervisorAgent": "You are the support supervisor. Handle escalations and unresolved issues. Route non-escalations back to SupportCoordinator.",
}


async def run_handoff_example() -> str:
    client = OpenAIChatClient()
    agents = {
        name: client.as_agent(
            name=name,
            instructions=instr,
            require_per_service_call_history_persistence=True,
        )
        for name, instr in AGENTS_CONFIG.items()
    }
    triage, billing, technical, supervisor = agents.values()

    workflow = (
        HandoffBuilder(
            name="af_handoff",
            participants=list(agents.values()),
            termination_condition=lambda conv: sum(1 for m in conv if m.role == "user") >= 4,
        )
        .with_start_agent(triage)
        .add_handoff(triage, [billing, technical, supervisor])
        .add_handoff(billing, [technical, triage])
        .add_handoff(technical, [billing, triage])
        .add_handoff(supervisor, [triage])
        .build()
    )

    events = [e async for e in workflow.run(CUSTOMER_PROMPT, stream=True)]
    scripted_iter = iter(SCRIPTED_RESPONSES)

    while pending := [e for e in events if e.type == "request_info" and isinstance(e.data, HandoffAgentUserRequest)]:
        user_reply = next(scripted_iter, "Thanks, that's all.")
        responses = {req.request_id: [Message(role="user", contents=[user_reply])] for req in pending}
        events = [e async for e in workflow.run(stream=True, responses=responses)]

    for event in events:
        if event.type == "output":
            messages = cast(list[Message], event.data)
            return "\n".join(
                f"{m.author_name or m.role}: {m.text}"
                for m in messages if m.text and m.text.strip()
            )
    return ""


async def main() -> None:
    print("===== Agent Framework Handoff =====")
    print(await run_handoff_example() or "No output produced.")


if __name__ == "__main__":
    asyncio.run(main())