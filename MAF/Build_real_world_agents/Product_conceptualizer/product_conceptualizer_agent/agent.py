from datetime import datetime
from typing import Dict, List, Any
import asyncio
from google.adk.agents import LlmAgent

# Product Conceptualizer Tool
def generate_product_concept_tool(
    business_type: str,
    target_audience: str,
    brand_values: List[str],
) -> Dict[str, Any]:
    """
    TOOL: Provides structured context back to LLM so it can fill product concept.
    """
    print(f"DEBUG (Concept Tool): Creating product concept for '{business_type}' targeting '{target_audience}'...")

    return {
        "status": "success",
        "inputs": {
            "business_type": business_type,
            "target_audience": target_audience,
            "brand_values": brand_values,
            "concept_generated_on": datetime.now().strftime("%Y-%m-%d"),
        },
    }



# ADK Agent Definition
def create_conceptualizer_agent() -> LlmAgent:
    """Constructs and returns the Product Conceptualizer Agent with streaming support."""
    return LlmAgent(
        model="gemini-2.5-flash",
        name="product_conceptualizer",
        instruction=f"""**Role:** You are the Product Conceptualizer Agent.  
Your responsibility is to transform an initial **specific product idea** into a **unique, fully developed product concept** with structured details.  

**Workflow Responsibilities:**  
1. Call **generate_product_concept_tool** to gather inputs.
2. Use them to create a complete product concept dictionary with:
   - `product_name`, `tagline`, `description`, `unique_selling_points`, `concept_generated_on`
3. If running in streaming mode, send intermediate updates as partial events, then send the final output.

**Important Rules:**  
- No generic placeholders: every field must be product-specific.
- Final response must be a well-formed dictionary, never free text.
- Do not ask any clarifying questions; work with the provided inputs only.  
""",
        tools=[generate_product_concept_tool],
    )


# Expose root_agent so the agent server can find it
root_agent = create_conceptualizer_agent()
