from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseTool(ABC):
    """
    工具基类，定义所有工具的标准接口。
    所有具体工具实现应该继承此类。
    """
    
    def __init__(self, name: str, description: str):
        """
        初始化工具。
        
        Args:
            name: 工具名称
            description: 工具功能描述
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, input_data: str) -> str:
        """
        执行工具功能。
        
        Args:
            input_data: 工具输入参数
            
        Returns:
            工具执行结果
        """
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        获取工具元数据。
        
        Returns:
            包含工具名称和描述的字典
        """
        return {
            "name": self.name,
            "description": self.description
        }
