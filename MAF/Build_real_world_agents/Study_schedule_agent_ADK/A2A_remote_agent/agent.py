from datetime import datetime
from typing import Dict, List, Any
import asyncio
from google.adk.agents import LlmAgent

# --- Study schedule generator ---
def generate_study_schedule_tool(
    subject: str,
    study_duration: int,
    learning_style: str,
    calendar: dict,
) -> Dict[str, Any]:
    """
    TOOL: Provides structured context back to LLM so it can fill product concept.
    """
    print(f"DEBUG (Concept Tool): Creating study schedule for '{subject}'...")

    return {
        "status": "success",
        "inputs": {
            "subject": subject,
            "study_duration": study_duration,
            "learning_style": learning_style,
            "calendar": calendar,
        },
    }



# --- ADK Agent Definition ---
def study_schedule_agent() -> LlmAgent:
    """Constructs and returns the Study Schedule Agent with streaming support."""
    return LlmAgent(
        model="gemini-2.5-flash",
        name="study_schedule_agent",
        instruction=f"""**Role:** You are the Study Schedule Agent.  
Your responsibility is to transform an initial **specific study schedule** into a **unique, fully developed study plan** with structured details considering the calendar.  

**Workflow Responsibilities:**  
1. Call **generate_study_schedule_tool** to gather inputs.
2. Use them to create a complete study plan dictionary with:
   - `subject`, `study_duration`, `learning_style`, `calendar`
3. If running in streaming mode, send intermediate updates as partial events, then send the final output.
4. The study schedule should incorporate the tasks provided in the calendar.
5. Each hour should tell which task to do.

**Important Rules:**  
- No generic placeholders: every field must be product-specific.
- Final response must be a well-formed dictionary, never free text.
""",
        tools=[generate_study_schedule_tool],
    )


# Expose root_agent so the agent server can find it
root_agent = study_schedule_agent()
