import os

from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.genai import types
from veadk import Agent, Runner
from veadk.a2a.remote_ve_agent import RemoteVeAgent
from veadk.config import getenv
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.demo_tools import get_city_weather
from veadk.utils.mcp_utils import get_mcp_params

short_term_memory = ShortTermMemory(backend="local")

###Shopping cart MCP Server
shopping_mcp_tools_url = getenv("SHOPPING_CART_MCP_TOOLS_URL")
shopping_api_key = getenv("SHOPPING_CART_MCP_API_KEY")
mcp_shopping_cart = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
        url=shopping_mcp_tools_url,
        headers={"Authorization": f"Bearer {shopping_api_key}"},
    ),
)

agent_model_name=getenv("MODEL_AGENT_NAME")

agent: Agent = Agent(
    name="shopping_cart_advanced",
    model_name=agent_model_name,
    instruction="You are an shopping cart agent.",
    #planner=PlanReActPlanner(),
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
        ),
    ),
    tools=[mcp_shopping_cart],
    short_term_memory=short_term_memory,
)

root_agent = agent