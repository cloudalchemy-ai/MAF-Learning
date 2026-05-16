# MAF RAG Agent — pip install agent-framework chromadb azure-identity python-dotenv

import asyncio, chromadb
from dotenv import load_dotenv
from agent_framework import Agent, ContextProvider, Message
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential

load_dotenv()

POLICY_DOCUMENT = "/Users/kshitijjoy_1/Documents/maf-course-v1/MAF/Build_real_world_agents/Doc-Insights/company_policy.md"

# ── RAG Context Provider (retrieve only — as minimal as it gets) ───

class RAGProvider(ContextProvider):
    def __init__(self, col):
        super().__init__("rag")
        self._col = col

    async def before_run(self, *, agent, session, context, state):
        query = " ".join(m.text for m in context.input_messages if m and m.text)
        results = self._col.query(query_texts=[query], n_results=3, include=["documents"])
        context.extend_messages(self.source_id, [
            Message(role="user", contents=["\n---\n".join(results["documents"][0])])
        ])

# ── Ingestion + Agent ─────────────────────────────────────────────

async def main():
    # Ingest: chunk → embed → store (ChromaDB handles embedding automatically)
    col = chromadb.Client().get_or_create_collection("docs")
    text = open(POLICY_DOCUMENT).read()
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    col.upsert(ids=[f"p::{i}" for i in range(len(chunks))], documents=chunks)

    # Agent with RAG
    agent = Agent(
        client=FoundryChatClient(credential=DefaultAzureCredential()),
        name="rag-agent",
        instructions="Answer ONLY from the provided context. Say 'I don't know' if not covered.",
        context_providers=[RAGProvider(col)],
    )

    while (q := input("You: ").strip()) not in ("quit", "exit"):
        print(f"Agent: {await agent.run(q)}\n")

if __name__ == "__main__":
    asyncio.run(main())