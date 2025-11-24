import os
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.db.postgres import PostgresDb
from agno.vectordb.pgvector import PgVector, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.models.openai import OpenAILike


# Set up knowledge base
meeting_kb = Knowledge(
    contents_db=PostgresDb(
        id="meeting_kb",
        db_url=os.getenv("POSTGRES_DB_URL"),
        knowledge_table="meeting_contents",
    ),
    vector_db=PgVector(
        id="meeting_vector",
        table_name="meeting_vector",
        db_url=os.getenv("POSTGRES_DB_URL"),
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(
            id=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            dimensions=1024,
        )
    ),
)

local_dir = os.path.dirname(__file__)
system_prompt_path = os.path.join(local_dir, "config", "counselor_prompt.md")
with open(system_prompt_path, "r", encoding='utf-8') as f:
    system_prompt = f.read()

# Create your agent
qwen_model = OpenAILike(
    id=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

sessions_db = PostgresDb(
    id="sessions_db",
    db_url=os.getenv("POSTGRES_DB_URL"),
    session_table="sessions",
)

counselor_agent = Agent(
    model=qwen_model,
    name="counselor_agent",
    description="A counselor agent that counsels the meeting",
    db=sessions_db,
    add_history_to_context=True,
    num_history_runs=50,
    knowledge=meeting_kb,
    search_knowledge=True,
    instructions=[system_prompt],
    enable_agentic_knowledge_filters=True,
    debug_mode=os.getenv("AGNO_DEBUG_MODE", False),
)

# Chat with your agent
if __name__ == "__main__":
    meeting_kb.add_content(
        path="./sample.txt",
        skip_if_exists=True,
    )

    counselor_agent.print_response("本次会议主要讨论了哪些内容？", stream=True)
