import uuid
from collections.abc import AsyncIterable
from typing import Any

from crewai import Agent, Crew, Task
from crewai.process import Process
from crewai.tools import tool

import logging
import uuid
import requests
from typing import Any
from pydantic import BaseModel
from crewai import Agent, Crew, Task
from crewai.process import Process
from dotenv import load_dotenv
from .utils import cache  

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Business Idea Generator Tool using N8N webhook

@tool
def generate_business_idea_tool(prompt: str, session_id: str) -> str:
    """
    Generates a business idea by calling an N8N workflow.
    Expects N8N webhook URL to be set as environment variable N8N_WEBHOOK_URL.
    Returns the raw response.text from N8N.
    """
    import os
    N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

    logger.info(f'### [Generator] Called with prompt="{prompt}" and session_id="{session_id}"')

    if not prompt:
        raise ValueError('Prompt cannot be empty')

    if not N8N_WEBHOOK_URL:
        raise ValueError('N8N_WEBHOOK_URL environment variable is not set')

    try:
        #prepare payload with user input and session
        payload = {"prompt": prompt, "session_id": session_id}
        logger.info(f'### [Generator] Sending payload to N8N: {payload}')

        #send request to N8N workflow
        response = requests.post(N8N_WEBHOOK_URL, json=payload)

        logger.info(f'### [Generator] N8N responded with status {response.status_code}')

        #check for success
        if response.status_code != 200:
            raise ValueError(f"N8N returned status {response.status_code}: {response.text}")

        #generate unique ID
        idea_text = response.text
        idea_id = uuid.uuid4().hex
        logger.info(f'### [Generator] Generated idea ID={idea_id}')
        logger.info(f'### [Generator] Raw N8N output (type={type(idea_text)}): {idea_text}')
        print(f"#####{idea_text}#####")
        return idea_text

    except Exception as e:
        logger.error(f'### [Generator] Error generating business idea: {e}')
        return "Error generating idea"

#Business Idea agent - Using CrewAI
class BusinessIdeaAgent:
    SUPPORTED_CONTENT_TYPES = ['text/plain', 'application/json']

    def __init__(self):
        self.validator_agent = Agent(
            role='Business Validator Agent',
            goal='Validate business ideas.',
            backstory='You are an expert in business idea validation.',
            verbose=False,
            allow_delegation=False,
            tools=[generate_business_idea_tool],
        )

        self.validation_task = Task(
            description=(
                "You are given a business idea: '{user_prompt}'.\n"
                "Pass it to the `generate_business_idea_tool` for idea generation.\n"
                "Print and Evaluate the generated idea for:\n"
                "1. Market demand\n"
                "2. Uniqueness and differentiation\n"
                "3. Scalability\n"
                "4. Revenue potential\n"
                "5. Risks and challenges\n\n"
                "Use session ID: '{session_id}' when calling the tool."
            ),
            expected_output='A short and structured validation report of the business idea',
            agent=self.validator_agent,
        )
        #crew is agent+task+sequential process
        self.validator_crew = Crew(
            agents=[self.validator_agent],
            tasks=[self.validation_task],
            process=Process.sequential,
            verbose=False,
        )
    
    #runs the workflow
    def invoke(self, prompt: str, session_id: str) -> str:
        session_id = session_id or f'session-{uuid.uuid4().hex}'
        logger.info(
            f'[invoke] Using session_id: {session_id} for query: {prompt}'
        )

        inputs = {
            "user_prompt": prompt,
            "session_id": session_id
        }

        response = self.validator_crew.kickoff(inputs)
        logger.info(
            f'[invoke] Final response: {response}'
        )
        return response
    
    async def stream(self, query: str) -> AsyncIterable[dict[str, Any]]:
        raise NotImplementedError('Streaming is not supported.')