#!/usr/bin/env python3
"""
基于智谱AI的FigureYa智能RAG系统
使用GLM-4大语言模型
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict
import numpy as np
from dataclasses import dataclass

@dataclass
class ZhipuAIConfig:
    """智谱AI配置"""
    api_key: str = ""
    model: str = "glm-4-flash"  # 免费模型
    embedding_model: str = "embedding-2"

    # RAG配置
    chunk_size: int = 500
    top_k: int = 5
    similarity_threshold: float = 0.7

class ZhipuAIRAG:
    """基于智谱AI的RAG系统"""

    def __init__(self, config: ZhipuAIConfig):
        self.config = config
        self.figureya_path = Path("/Users/mypro/Downloads/FigureYa")
        self.knowledge_base = self._build_knowledge_base()

        # 初始化智谱AI客户端
        try:
            from zhipuai import ZhipuAI
            self.client = ZhipuAI(api_key=config.api_key)
        except ImportError:
            print("❌ 请安装智谱AI SDK: pip install zhipuai")
            self.client = None

    def _build_knowledge_base(self) -> dict:
        """构建知识库"""
        return {
            "差异表达分析": {
                "modules": ["FigureYa59volcanoV2", "FigureYa9heatmap"],
                "description": "识别不同条件间基因表达差异",
                "methods": ["DESeq2", "edgeR", "limma"],
                "keywords": ["RNA-seq", "差异基因", "火山图", "热图"]
            },
            "生存分析": {
                "modules": ["FigureYa36nSurvV3", "FigureYa1survivalCurve_update"],
                "description": "分析患者生存时间和影响因素",
                "methods": ["Kaplan-Meier", "Cox回归"],
                "keywords": ["生存", "预后", "风险比", "Kaplan-Meier"]
            },
            "单细胞分析": {
                "modules": ["FigureYa274MuSiCbulkProop", "FigureYa243scMarkerGroupHeatmap"],
                "description": "单个细胞水平的基因表达分析",
                "methods": ["质控", "降维", "聚类", "差异分析"],
                "keywords": ["单细胞", "scRNA-seq", "UMAP", "tSNE", "聚类"]
            },
            "PCA分析": {
                "modules": ["FigureYa38PCA", "FigureYa164PCA3D"],
                "description": "高维数据的降维和可视化",
                "methods": ["主成分分析", "奇异值分解"],
                "keywords": ["PCA", "主成分", "降维", "可视化"]
            }
        }

    def intelligent_search(self, query: str) -> dict:
        """智能搜索和回答"""
        if not self.client:
            return self._fallback_response(query)

        # 检索相关知识
        relevant_info = self._retrieve_knowledge(query)

        # 生成智能回答
        response = self._generate_zhipuai_response(query, relevant_info)

        return {
            "query": query,
            "response": response,
            "sources": [info.get("modules", []) for info in relevant_info],
            "model": self.config.model,
            "ai_enhanced": True
        }

    def _retrieve_knowledge(self, query: str) -> List[dict]:
        """检索相关知识"""
        query_lower = query.lower()
        relevant = []

        for topic, info in self.knowledge_base.items():
            score = 0

            # 关键词匹配
            for keyword in info.get("keywords", []):
                if keyword.lower() in query_lower:
                    score += 2

            # 方法匹配
            for method in info.get("methods", []):
                if method.lower() in query_lower:
                    score += 3

            # 模块匹配
            for module in info.get("modules", []):
                if module.lower() in query_lower:
                    score += 1

            if score > 0:
                relevant.append({"topic": topic, **info, "score": score})

        # 按分数排序
        relevant.sort(key=lambda x: x["score"], reverse=True)
        return relevant[:3]

    def _generate_zhipuai_response(self, query: str, relevant_info: List[dict]) -> str:
        """使用智谱AI生成回答"""
        if not relevant_info:
            return "抱歉，我在知识库中没有找到相关信息。请尝试使用更具体的关键词。"

        # 构建上下文
        context = "\n\n".join([
            f"主题: {info['topic']}\n模块: {', '.join(info['modules'])}\n描述: {info['description']}\n方法: {', '.join(info['methods'])}"
            for info in relevant_info
        ])

        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一个专业的生物医学数据分析专家，基于FigureYa知识库回答用户问题。

请根据提供的上下文信息，专业、准确地回答用户问题。要求：
1. 基于上下文信息，提供专业建议
2. 给出具体的分析步骤和参数建议
3. 使用中文回答
4. 保持专业但易懂的语气"""
                    },
                    {
                        "role": "user",
                        "content": f"用户问题：{query}\n\n相关知识：\n{context}\n\n请基于以上信息回答用户问题。"
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"⚠️ 智谱AI API调用失败: {e}")
            return self._fallback_response(query)

    def _fallback_response(self, query: str) -> str:
        """备用回答"""
        relevant_info = self._retrieve_knowledge(query)
        if relevant_info:
            best = relevant_info[0]
            return f"""基于您的查询，我推荐以下模块：

🎯 **推荐模块**: {', '.join(best['modules'])}
📝 **功能描述**: {best['description']}
🔬 **技术方法**: {', '.join(best['methods'])}

💡 这是一个基础的推荐结果。配置智谱AI API后可以获得更专业的个性化建议。"""

        return "抱歉，我没有找到相关信息。请尝试使用更具体的关键词。"

def main():
    """主函数"""
    print("🧠 FigureYa 智谱AI RAG系统")
    print("=" * 40)

    # 加载API密钥
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ 未找到智谱AI API密钥")
        print("💡 请设置环境变量: export ZHIPUAI_API_KEY='your-key'")
        return

    # 初始化系统
    config = ZhipuAIConfig(api_key=api_key)
    rag = ZhipuAIRAG(config)

    print("🎯 智能问答演示:")
    print("-" * 50)

    # 测试查询
    test_queries = [
        "RNA-seq差异表达分析推荐什么模块？",
        "生存分析的方法有哪些？",
        "单细胞分析的关键步骤是什么？"
    ]

    for query in test_queries:
        print(f"\n❓ 查询: {query}")
        result = rag.intelligent_search(query)
        print(f"💬 回答: {result['response'][:200]}...")
        print(f"🤖 AI模型: {result['model']}")
        print("-" * 30)

if __name__ == "__main__":
    main()
