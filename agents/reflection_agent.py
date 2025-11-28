from core import Agent
from typing import List, Dict, Any, Optional



DEFAULT_PROMPTS = {
    "initial": """
请根据以下任务要求给出回答：

{task}

注意：
- 如果任务要求编写代码/函数，请提供Python代码
- 如果任务是问答/写文章/分析等，请直接给出文字内容，不要用代码包装
- 确保回答完整、准确、实用
""",
    "reflect": """
请仔细审查以下回答，并找出可能的问题或改进空间:

# 原始任务:
{task}

# 当前回答:
{content}

请分析这个回答的质量，指出不足之处，并提出具体的改进建议。
重要提示：
1.如果回答已经很好，请直接回答"无需改进"。在其他情况下不可以回答这个选项
2.如果回答有缺陷，请详细说明问题所在，并给出改进建议。
""",
    "refine": """
请根据反馈意见改进你的回答:

# 原始任务:
{task}

# 上一轮回答:
{last_attempt}

# 反馈意见:
{feedback}

重要要求：
1. 只改进内容质量，不要改变输出格式
2. 如果上一轮回答是纯文本/Markdown格式，继续使用纯文本/Markdown，不要用```python或函数包装
3. 如果上一轮回答是Python代码，继续使用代码格式
4. 保持原有的结构和呈现方式，只优化具体内容

请直接输出改进后的回答：
"""
}




class Memory:
    """
    一个简单的短期记忆模块，用于存储智能体的行动与反思轨迹。
    """

    def __init__(self):
        """
        初始化一个空列表来存储所有记录。
        """
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, content: str):
        """
        向记忆中添加一条新记录。

        参数:
        - record_type (str): 记录的类型 ('execution' 或 'reflection')。
        - content (str): 记录的具体内容 (例如，生成的代码或反思的反馈)。
        """
        record = {"type": record_type, "content": content}
        self.records.append(record)
        print(f"📝 记忆已更新，新增一条 '{record_type}' 记录。")

    def get_trajectory(self) -> str:
        """
        将所有记忆记录格式化为一个连贯的字符串文本，用于构建提示词。
        """
        trajectory_parts = []
        for record in self.records:
            if record['type'] == 'execution':
                trajectory_parts.append(f"--- 上一轮尝试 (代码) ---\n{record['content']}")
            elif record['type'] == 'reflection':
                trajectory_parts.append(f"--- 评审员反馈 ---\n{record['content']}")
        
        return "\n\n".join(trajectory_parts)

    def get_last_execution(self) -> Optional[str]:
        """
        获取最近一次的执行结果 (例如，最新生成的代码)。
        如果不存在，则返回 None。
        """
        for record in reversed(self.records):
            if record['type'] == 'execution':
                return record['content']
        return None



class ReflectionAgent(Agent):
    def __init__(self, llm_client, custom_prompts = None, max_iterations=3):
        super().__init__(name="Reflection Agent", llm=llm_client)
        self.llm_client = llm_client
        self.memory = Memory()
        self.max_iterations = max_iterations
        self.custom_prompts = DEFAULT_PROMPTS
        if  custom_prompts is not None:
            self.custom_prompts["initial"] = custom_prompts["initial"] or DEFAULT_PROMPTS["initial"]
            self.custom_prompts["reflect"] = custom_prompts["reflect"] or DEFAULT_PROMPTS["reflect"]
            self.custom_prompts["refine"] = custom_prompts["refine"] or DEFAULT_PROMPTS["refine"]

    def run(self, task: str):
        print(f"\n--- 开始处理任务 ---\n任务: {task}")

        # --- 1. 初始执行 ---
        print("\n--- 正在进行初始尝试 ---")
        initial_prompt = self.custom_prompts["initial"].format(task=task)
        initial_code = self._get_llm_response(initial_prompt)
        self.memory.add_record("execution", initial_code)

        # --- 2. 迭代循环:反思与优化 ---
        for i in range(self.max_iterations):
            print(f"\n--- 第 {i+1}/{self.max_iterations} 轮迭代 ---")

            # a. 反思
            print("\n-> 正在进行反思...")
            last_answer = self.memory.get_last_execution()
            reflect_prompt = self.custom_prompts["reflect"].format(task=task, content=last_answer)
            feedback = self._get_llm_response(reflect_prompt)
            self.memory.add_record("reflection", feedback)

            # b. 检查是否需要停止
            # 检查是否明确表示无需改进（句首或独立行）
            feedback_lines = feedback.strip().split('\n')
            should_stop = any(
                line.strip() in ["无需改进", "无需修改", "完美实现"] or
                line.strip().startswith("无需改进") or
                line.strip().startswith("无需修改")
                for line in feedback_lines
            )
            if should_stop:
                print("\n✅ 反思认为回答已达到高质量标准，任务完成。")
                break

            # c. 优化
            print("\n-> 正在进行优化...")
            refine_prompt = self.custom_prompts["refine"].format(
                task=task,
                last_attempt=last_answer,
                feedback=feedback
            )
            refined_code = self._get_llm_response(refine_prompt)
            self.memory.add_record("execution", refined_code)
        
        final_answer = self.memory.get_last_execution()
        print(f"\n--- 任务完成 ---\n最终生成的结果:\n\n{final_answer}")
        return final_answer

    def _get_llm_response(self, prompt: str) -> str:
        """一个辅助方法，用于调用LLM并获取完整的流式响应。"""
        messages = [{"role": "user", "content": prompt}]
        response_text = self.llm_client.invoke(messages=messages) or ""
        return response_text

