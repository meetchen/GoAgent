"""
GoAgent Core 核心模块

这个包包含了 GoAgent 框架的核心组件：
- Agent: Agent 抽象基类
- Message: 消息类
- GoAgentLLM: 大语言模型客户端
- Config: 配置管理类
"""

from .agent import Agent
from .message import Message, MessageRole
from .go_agent_llm import GoAgentLLM
from .config import Config

# 定义模块的公开接口
# 当使用 from core import * 时，只会导入这些
__all__ = [
    "Agent",
    "Message",
    "MessageRole",
    "GoAgentLLM",
    "Config",
]

# 版本信息
__version__ = "0.1.0"
