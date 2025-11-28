from typing import Dict, Any, Optional, List, Callable
from .base import BaseTool


class ToolExecutor:
    """
    工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
    
    def register_tool(self, tool: BaseTool) -> None:
        """
        向工具箱中注册一个新工具。
        
        Args:
            tool: 实现了BaseTool接口的工具实例
        """
        if tool.name in self.tools:
            print(f"警告: 工具 '{tool.name}' 已存在，将被覆盖。")
        self.tools[tool.name] = tool
        print(f"工具 '{tool.name}' 已注册。")
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        根据名称获取一个工具。
        
        Args:
            name: 工具名称
            
        Returns:
            工具实例，如不存在则返回None
        """
        return self.tools.get(name)
    
    def execute_tool(self, name: str, input_data: str) -> str:
        """
        执行指定名称的工具。
        
        Args:
            name: 工具名称
            input_data: 工具输入参数
            
        Returns:
            工具执行结果
        """
        tool = self.get_tool(name)
        if tool:
            return tool.execute(input_data)
        return f"错误: 未找到名为 '{name}' 的工具。"
    
    def get_available_tools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        
        Returns:
            工具列表的格式化字符串
        """
        return "\n".join([
            f"- {name}: {tool.description}" 
            for name, tool in self.tools.items()
        ])
    
    def get_tools_metadata(self) -> List[Dict[str, Any]]:
        """
        获取所有工具的元数据列表。
        
        Returns:
            工具元数据列表
        """
        return [tool.get_metadata() for tool in self.tools.values()]

    def get_tools_description(self) -> str:
        """
        获取所有工具的描述字符串。
        
        Returns:
            工具描述字符串
        """
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"{name}: {tool.description}")
        return "\n".join(descriptions)
