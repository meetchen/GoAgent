import sys
import os
# 添加项目根目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from core import GoAgentLLM
from agents import PlanAndSolveAgent

# 加载环境变量
load_dotenv()

# 初始化组件
llm_client = GoAgentLLM()


# 创建专门用于数学问题的自定义提示词
math_prompts = {
    "planner": """
你是数学问题规划专家。请将数学问题分解为计算步骤:

问题: {question}

输出格式:
python
["计算步骤1", "计算步骤2", "求总和"]

""",
    "executor": """
你是数学计算专家。请计算当前步骤:

问题: {question}
计划: {plan}
历史: {history}
当前步骤: {current_step}

请只输出数值结果:
"""
}

# 使用自定义提示词创建数学专用Agent
# math_agent = PlanAndSolveAgent(
#     llm_client=llm_client,
#     custom_prompt=math_prompts
# )

# question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
# # 测试数学问题
# math_result = math_agent.run(question)
# print(f"数学专用Agent结果: {math_result}")


# 创建通用的Plan and Solve智能体（使用默认提示词）  
plan_and_solve_agent = PlanAndSolveAgent(
    llm_client=llm_client,
)
# 运行测试 - 可以切换不同的问题
# question = "请写一首关于春天的诗"
question = "请帮我制定一个一周的健身计划，目标是增肌和减脂，每天锻炼时间控制在1小时以内。"
# question = "请解释一下量子计算的基本原理，并举例说明它在现实生活中的应用。"
plan_and_solve_result = plan_and_solve_agent.run(question)
print(f"Plan and Solve Agent结果: {plan_and_solve_result}")
