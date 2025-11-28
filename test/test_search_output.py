#!/usr/bin/env python3
"""
测试搜索工具的输出格式
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from tools import SearchTool

# 加载环境变量
load_dotenv()

# 创建搜索工具
search_tool = SearchTool()

# 测试搜索
print("=" * 80)
print("测试搜索工具输出格式")
print("=" * 80)

query = "Python programming language"
result = search_tool.execute(query)

print("\n搜索结果:")
print(result)
print("\n" + "=" * 80)
