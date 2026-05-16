from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    InvalidParamsError,
    Part,
    Task,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    completed_task,
    new_artifact,
)
from a2a.utils.errors import ServerError
from .agent import BusinessIdeaAgent   

#business idea agent executor
class BusinessIdeaAgentExecutor(AgentExecutor):  
    def __init__(self):
        # Create instance of our BusinessIdeaAgent (from agent.py)
        self.agent = BusinessIdeaAgent()  

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Validate incoming request before processing
        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())

        # Get user input from request context
        query = context.get_user_input()
        try:
            result = self.agent.invoke(query, context.context_id)  
        except Exception as e:
            raise ServerError(
                error=ValueError(f'Error invoking agent: {e}')
            ) from e

        # Prepare formatted plain-text output for the final response
        text_output = f"💡 Business Idea Result:\n{result}"

        # Wrap result into A2A "Part" structure for returning artifacts
        parts = [
            Part(
                root=TextPart(text=text_output),
            )
        ]

        # Send "completed task" event with result back to event queue
        await event_queue.enqueue_event(
            completed_task(
                context.task_id,
                context.context_id,
                [new_artifact(parts, f'idea_{context.task_id}')],  
            )
        )

    # If cancel request is received → not supported for now
    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())

    # Request validation placeholder → currently always returns False
    def _validate_request(self, context: RequestContext) -> bool:
        return False
