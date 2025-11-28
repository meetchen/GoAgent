import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Optional

# 加载 .env 文件中的环境变量
load_dotenv()


class GoAgentLLM:
    """
    大语言模型客户端。
    用于调用任何兼容OpenAI接口的服务，并默认使用流式响应。
    """
    def __init__(self, model: str = None, api_key: str = None, base_url: str = None, timeout: int = None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。
        
        Args:
            model: 模型ID，默认从环境变量LLM_MODEL_ID获取
            api_key: API密钥，默认从环境变量LLM_API_KEY获取
            base_url: 服务地址，默认从环境变量LLM_BASE_URL获取
            timeout: 超时时间(秒)，默认从环境变量LLM_TIMEOUT获取，若未设置则为60秒
        """
        self.model = model or os.getenv("LLM_MODEL_ID")
        api_key = api_key or os.getenv("LLM_API_KEY")
        base_url = base_url or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))
        
        if not all([self.model, api_key, base_url]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    def invoke(self, messages: List[Dict[str, str]], temperature: float = 0, **kwargs) -> Optional[str]:
        """
        调用大语言模型生成回复，并返回其响应。
        
        Args:
            messages: 对话历史消息列表
            temperature: 温度参数，控制回复的随机性，默认为0(最确定性)
            **kwargs: 其他参数（为了兼容性，当前会被忽略）
            
        Returns:
            模型生成的文本，如出错则返回None
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            
            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None
    
    def stream_invoke(self, messages: List[Dict[str, str]], temperature: float = 0, **kwargs):
        """
        流式调用大语言模型，逐块返回响应内容（生成器）。
        
        Args:
            messages: 对话历史消息列表
            temperature: 温度参数，控制回复的随机性，默认为0(最确定性)
            **kwargs: 其他参数（为了兼容性，当前会被忽略）
            
        Yields:
            每次生成的文本块
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                if content:
                    yield content
                    
        except Exception as e:
            print(f"❌ 流式调用LLM API时发生错误: {e}")
            yield ""
