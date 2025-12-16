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

#amap_mcp_api_key
amap_mcp_tool_set_api_key = getenv("AMAP_MCP_TOOL_SET_API_KEY")
amap_mcp_tool_set_url = getenv("AMAP_MCP_TOOL_SET_URL")
amap_mcp_tool_set = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
        url=amap_mcp_tool_set_url,
        headers={"Authorization": f"Bearer {amap_mcp_tool_set_api_key}"},
    ),
)

agent_model_name=getenv("MODEL_AGENT_NAME")

agent: Agent = Agent(
    name="amap_tool_set_agent",
    model_name=agent_model_name,
    instruction="You are an map agent.",
    #planner=PlanReActPlanner(),
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
        ),
    ),
    tools=[amap_mcp_tool_set],
    short_term_memory=short_term_memory,
)

root_agent = agent
