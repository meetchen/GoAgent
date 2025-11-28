import sys
import os
# 添加项目根目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from core import GoAgentLLM
from agents import ReflectionAgent

# 加载环境变量
load_dotenv()

# 初始化组件
llm_client = GoAgentLLM()


# 创建Reflection智能体（使用默认提示词）
reflection_agent = ReflectionAgent(llm_client=llm_client, max_iterations=50)

# 运行测试 - 可以切换不同的问题
# question = "请编写一个Python函数，计算斐波那契数列的第n个数"
question = "我现在有一个4070tis显卡，我可以本地部署哪些模型？"
# question = "写一篇关于人工智能发展历程的简短文章"

result = reflection_agent.run(question)
