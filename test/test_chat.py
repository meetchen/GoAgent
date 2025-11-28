# test_simple_agent.py
import sys
import os
# 添加项目根目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from core import GoAgentLLM
from agents.chat_agent import ChatAgent

# 加载环境变量
load_dotenv()

# 创建LLM实例
llm = GoAgentLLM()

# 测试1:基础对话Agent（无工具）
print("=== 测试1:基础对话 ===")
basic_agent = ChatAgent(
    name="基础助手",
    llm=llm,
    system_prompt="你是一个友好的AI助手，请用简洁明了的方式回答问题。"
)

response1 = basic_agent.run("你好，请介绍一下自己")
print(f"\n基础对话响应: {response1}\n")

# 测试2: 继续对话（测试历史记录）
print("=== 测试2:对话历史 ===")
response2 = basic_agent.run("我刚才问了你什么问题？")
print(f"\n对话响应: {response2}\n")

# 查看对话历史
print("=== 测试3:查看历史记录 ===")
history = basic_agent.get_history()
print(f"对话历史记录数: {len(history)} 条消息")
for i, msg in enumerate(history, 1):
    print(f"  {i}. [{msg.role}] {msg.content[:50]}{'...' if len(msg.content) > 50 else ''}")

# 测试4: 清空历史
print("\n=== 测试4:清空历史 ===")
basic_agent.clear_history()
print(f"清空后历史记录数: {len(basic_agent.get_history())} 条消息")

print("\n✅ 基础测试完成！")
print("\n" + "="*50)
print("注意：工具调用功能需要先实现 ToolRegistry 和 Tool 类")
print("="*50)

# ====================================================
# 以下是工具相关测试（需要实现工具系统后取消注释）
# ====================================================

# # 测试5:带工具的Agent
# print("\n=== 测试5:工具增强对话 ===")
# from tools import ToolRegistry, CalculatorTool
# 
# tool_registry = ToolRegistry()
# calculator = CalculatorTool()
# tool_registry.register_tool(calculator)
# 
# enhanced_agent = MySimpleAgent(
#     name="增强助手",
#     llm=llm,
#     system_prompt="你是一个智能助手，可以使用工具来帮助用户。",
#     tool_registry=tool_registry,
#     enable_tool_calling=True
# )
# 
# response = enhanced_agent.run("请帮我计算 15 * 8 + 32")
# print(f"工具增强响应: {response}\n")
