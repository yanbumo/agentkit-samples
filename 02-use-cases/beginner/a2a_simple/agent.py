from veadk.a2a.remote_ve_agent import RemoteVeAgent
from veadk.agent import Agent
from veadk.memory import ShortTermMemory
from agentkit.app import AgentkitA2aApp
from a2a.types import AgentCard, AgentProvider, AgentSkill, AgentCapabilities

remote_agent = RemoteVeAgent(
    name="a2a_agent",
    url="http://localhost:8000/",  # <--- url from cloud platform
)

def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

agent = Agent(
    name="a2a_sample_agent",
    instruction="You are a helpful assistant.",
    tools=[add],
    sub_agents=[remote_agent],
)

a2aApp = AgentkitA2aApp(
    agent=agent,
    app_name="a2a_sample_app",
    short_term_memory=ShortTermMemory(),
)

if __name__ == "__main__":
    from a2a.types import AgentCard, AgentProvider, AgentSkill, AgentCapabilities
    
    agent_card = AgentCard(
        capabilities=AgentCapabilities(streaming=True),  # 启用流式
        description=agent.description,
        name=agent.name,
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        provider=AgentProvider(organization="veadk", url=""),
        skills=[AgentSkill(id="0", name="chat", description="Chat", tags=["chat"])],
        url="http://0.0.0.0:8000",
        version="1.0.0",
    )
    
    a2a_app.run(
        agent_card=agent_card,
        host="0.0.0.0",
        port=8000,
    )