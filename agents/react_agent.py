import re
from typing import List
from core import Agent, Message, GoAgentLLM
from tools import ToolExecutor

# ReAct 提示词模板 - 改进版，更明确的指令格式
REACT_PROMPT_TEMPLATE = """

你是一个具备推理和行动能力的AI助手。你可以通过思考分析问题，然后调用合适的工具来获取信息，最终给出准确的答案。

## 可用工具
{tools}

## 工作流程
请严格按照以下格式进行回应，每次只能执行一个步骤:

Thought: 分析当前问题，思考需要什么信息或采取什么行动。
Action: 选择一个行动，格式必须是以下之一:
- `{{tool_name}}[{{tool_input}}]` - 调用指定工具
- `Finish[最终答案]` - 当你有足够信息给出最终答案时

## 重要提醒
1. 每次回应必须包含Thought和Action两部分
2. 工具调用的格式必须严格遵循:工具名[参数]
3. 只有当你确信有足够信息回答问题时，才使用Finish
4. 如果工具返回的信息不够，继续使用其他工具或相同工具的不同参数

## 当前任务
**Question:** {question}

## 执行历史
{history}

现在开始你的推理和行动:
"""

class ReActAgent(Agent):
    def __init__(self, llm_client: GoAgentLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        super().__init__(name="ReAct Agent", llm=llm_client)
        self.llm_client = llm_client
        self.tool_registry = tool_executor
        self.max_steps = max_steps
        self.history = []
        self.name = "ReAct Agent"
        self.current_history: List[str] = []
        self.prompt_template = REACT_PROMPT_TEMPLATE

    def run(self, input_text: str, **kwargs) -> str:
        """运行ReAct Agent"""
        self.current_history = []
        current_step = 0

        print(f"\n🤖 {self.name} 开始处理问题: {input_text}")

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n--- 第 {current_step} 步 ---")

            # 1. 构建提示词
            tools_desc = self.tool_registry.get_tools_description()
            history_str = "\n".join(self.current_history)
            prompt = self.prompt_template.format(
                tools=tools_desc,
                question=input_text,
                history=history_str
            )

            # 2. 调用LLM
            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.invoke(messages, **kwargs)

            # 3. 解析输出
            thought, action = self._parse_output(response_text)
            
            # 显示思考过程
            if thought:
                print(f"\n💭 思考: {thought}")
            if action:
                print(f"⚡ 动作: {action}")

            # 4. 检查完成条件
            if action and action.startswith("Finish"):
                final_answer = self._parse_action_input(action)
                print(f"\n✅ 最终答案:")
                print(final_answer)
                self.add_message(Message(input_text, "user"))
                self.add_message(Message(final_answer, "assistant"))
                return final_answer

            # 5. 执行工具调用
            if action:
                tool_name, tool_input = self._parse_action(action)
                observation = self.tool_registry.execute_tool(tool_name, tool_input)
                print(f"\n📊 观察结果:")
                print(observation)
                print()
                self.current_history.append(f"Action: {action}")
                self.current_history.append(f"Observation: {observation}")

        # 达到最大步数
        final_answer = "抱歉，我无法在限定步数内完成这个任务。"
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_answer, "assistant"))
        return final_answer


    def _parse_output(self, text: str):
        """解析LLM的输出，提取Thought和Action。"""
        thought_match = re.search(r"Thought: (.*?)(?=\nAction:|\Z)", text, re.DOTALL)
        action_match = re.search(r"Action: (.*?)(?=\n\n|\Z)", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action: str):
        """解析Action，提取工具名称和输入参数。"""
        match = re.match(r"(\w+)\s*\[(.*)\]", action)
        if match:
            tool_name = match.group(1)
            tool_input = match.group(2)
            return tool_name, tool_input
        return None, None
    
    def _parse_action_input(self, action: str):
        """从Finish动作中提取最终答案。"""
        match = re.match(r"Finish\s*\[(.*)\]", action, re.DOTALL)
        if match:
            return match.group(1).strip()
        return action

