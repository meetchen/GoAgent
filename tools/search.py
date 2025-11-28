import os
from serpapi import SerpApiClient
from dotenv import load_dotenv
from .base import BaseTool

# 加载环境变量
load_dotenv()


class SearchTool(BaseTool):
    """
    基于SerpApi的网页搜索工具。
    智能解析搜索结果，优先返回直接答案或知识图谱信息。
    """
    
    def __init__(self):
        """初始化搜索工具"""
        super().__init__(
            name="Search",
            description="一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
        )
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            print("警告: SERPAPI_API_KEY 未在 .env 文件中配置。")
    
    def execute(self, query: str) -> str:
        """
        执行网页搜索。
        
        Args:
            query: 搜索查询字符串
            
        Returns:
            搜索结果文本
        """
        print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")
        try:
            if not self.api_key:
                return "错误: SERPAPI_API_KEY 未在 .env 文件中配置。"

            params = {
                "engine": "google",
                "q": query,
                "api_key": self.api_key,
                "gl": "cn",     # 国家代码
                "hl": "zh-cn",  # 语言代码
            }
            
            client = SerpApiClient(params)
            results = client.get_dict()
            
            # 智能解析:优先寻找最直接的答案
            if "answer_box_list" in results:
                answer_text = "【直接答案】\n" + "\n".join(results["answer_box_list"])
                return answer_text
            
            if "answer_box" in results and "answer" in results["answer_box"]:
                answer = results["answer_box"]["answer"]
                return f"【直接答案】\n{answer}"
            
            if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
                kg = results["knowledge_graph"]
                result_text = "【知识图谱】\n"
                if "title" in kg:
                    result_text += f"主题: {kg['title']}\n"
                result_text += f"描述: {kg['description']}"
                if "source" in kg:
                    result_text += f"\n来源: {kg['source']['name']}"
                return result_text
            if "organic_results" in results and results["organic_results"]:
                # 如果没有直接答案，则返回前三个有机结果的摘要
                total_results = len(results["organic_results"])
                snippets = []
                
                for i, res in enumerate(results["organic_results"][:3]):
                    title = res.get('title', '无标题')
                    snippet = res.get('snippet', '无描述')
                    link = res.get('link', '')
                    
                    result_text = f"【结果 {i+1}】\n"
                    result_text += f"📌 标题: {title}\n"
                    result_text += f"📄 摘要: {snippet}"
                    if link:
                        result_text += f"\n🔗 链接: {link}"
                    
                    snippets.append(result_text)
                
                header = f"🔎 搜索到 {total_results} 条结果，以下是前 {min(3, total_results)} 条:\n"
                separator = "\n" + "-"*60 + "\n"
                return header + separator.join(snippets)
            
            return f"对不起，没有找到关于 '{query}' 的信息。"

        except Exception as e:
            return f"搜索时发生错误: {e}"
