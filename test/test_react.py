import sys
import os
# 添加项目根目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from core import GoAgentLLM
from tools import ToolExecutor, SearchTool
from agents.react_agent import ReActAgent

# 加载环境变量
load_dotenv()

# 初始化组件
llm_client = GoAgentLLM()
tool_executor = ToolExecutor()

# 注册搜索工具
search_tool = SearchTool()
tool_executor.register_tool(search_tool)

# 创建ReAct智能体
react = ReActAgent(llm_client=llm_client, tool_executor=tool_executor, max_steps=10)

# 运行测试
question = "我是14600kf的cpu，我现在需要一块支持ddr4内存的主板，其次需要他支持多显卡，也就是pcie可以拆分为两条5.0*8"
result = react.run(question)

if not result:
    print(f"\n{Fore.RED}未能获得有效答案。{Style.RESET_ALL}")