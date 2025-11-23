from agno.os import AgentOS

from summarizer import summary_agent
from counselor import meeting_kb, counselor_agent

agent_os = AgentOS(
    description="An OS for the meeting assistant",
    agents=[summary_agent, counselor_agent],
    knowledge=[meeting_kb]
)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agno_os:app", reload=True)
