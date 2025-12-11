from veadk import Agent, Runner
from veadk.a2a.remote_ve_agent import RemoteVeAgent
from agentkit.apps import AgentkitA2aApp
from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor
from a2a.types import AgentCard, AgentProvider, AgentSkill, AgentCapabilities

remote_agent = RemoteVeAgent(
    name="a2a_agent",
    url="http://localhost:8001/",  # <--- url from remote agent service
)

def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

agent = Agent(
    name="a2a_sample_agent",
    instruction="You are a helpful assistant that can add numbers and delegate tasks to a remote agent that can roll dice and check prime numbers.",
    tools=[add],
    sub_agents=[remote_agent],
)

runner = Runner(agent=agent)


a2aApp = AgentkitA2aApp()

@a2aApp.agent_executor(runner=runner)
class MyAgentExecutor(A2aAgentExecutor):
    pass

if __name__ == "__main__":
    agent_card = AgentCard(
        capabilities=AgentCapabilities(streaming=True),
        description=agent.description,
        name=agent.name,
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        provider=AgentProvider(organization="agentkit", url=""),
        skills=[AgentSkill(id="0", name="chat", description="Chat", tags=["chat"])],
        url="http://0.0.0.0:8000",
        version="1.0.0",
    )

    a2aApp.run(
        agent_card=agent_card,
        host="0.0.0.0",
        port=8000,
    )