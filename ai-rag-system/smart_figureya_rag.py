#!/usr/bin/env python3
"""
真正智能的FigureYa RAG系统
集成现代LLM API和向量数据库
"""

import os
import json
import requests
import time
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass
import pickle
import hashlib

@dataclass
class RAGConfig:
    """RAG系统配置"""
    # OpenAI配置
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-ada-002"

    # 本地模型配置（备选）
    local_embedding_model: str = "all-MiniLM-L6-v2"
    local_llm_model: str = "llama3-8b"

    # 向量数据库配置
    vector_store_path: str = "figureya_vector_store.pkl"
    chunk_size: int = 500
    chunk_overlap: int = 50

    # 检索配置
    top_k: int = 5
    similarity_threshold: float = 0.7

class SmartFigureYaRAG:
    """真正智能的FigureYa RAG系统"""

    def __init__(self, config: RAGConfig = None):
        self.config = config or RAGConfig()
        self.figureya_path = Path("/Users/mypro/Downloads/FigureYa")
        self.vector_store = {}
        self.text_chunks = []
        self.embeddings = None

        # 检查API密钥
        self.api_available = self._check_apis()

    def _check_apis(self) -> Dict[str, bool]:
        """检查可用的API"""
        apis = {
            "openai": bool(self.config.openai_api_key),
            "sentence_transformer": False,
            "chromadb": False,
            "faiss": False
        }

        # 检查本地包
        try:
            import sentence_transformers
            apis["sentence_transformer"] = True
        except ImportError:
            pass

        try:
            import chromadb
            apis["chromadb"] = True
        except ImportError:
            pass

        try:
            import faiss
            apis["faiss"] = True
        except ImportError:
            pass

        return apis

    def load_knowledge_base(self):
        """加载并处理FigureYa知识库"""
        print("🧠 正在构建智能知识库...")

        # 加载文本文件
        texts_path = self.figureya_path / "texts"
        text_files = list(texts_path.glob("*.txt"))[:50]  # 限制数量以节省内存

        all_chunks = []
        for text_file in text_files:
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 智能分块
                chunks = self._smart_chunk_text(content, str(text_file))
                all_chunks.extend(chunks)

            except Exception as e:
                print(f"⚠️ 处理文件 {text_file} 时出错: {e}")

        self.text_chunks = all_chunks
        print(f"📚 已处理 {len(all_chunks)} 个文本块")

        # 生成embeddings
        self._generate_embeddings()

    def _smart_chunk_text(self, text: str, source: str) -> List[Dict]:
        """智能文本分块"""
        chunks = []

        # 按段落分块
        paragraphs = text.split('\n\n')
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) < self.config.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "source": source,
                        "word_count": len(current_chunk.split())
                    })
                current_chunk = paragraph + "\n\n"

        # 添加最后一个块
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "source": source,
                "word_count": len(current_chunk.split())
            })

        return chunks

    def _generate_embeddings(self):
        """生成文本embeddings"""
        print("🔍 正在生成向量表示...")

        if self.api_available["openai"] and self.config.openai_api_key:
            self._generate_openai_embeddings()
        elif self.api_available["sentence_transformer"]:
            self._generate_local_embeddings()
        else:
            print("❌ 没有可用的embedding模型")
            return

        print(f"✅ 已生成 {len(self.embeddings)} 个向量")

    def _generate_openai_embeddings(self):
        """使用OpenAI生成embeddings"""
        texts = [chunk["text"] for chunk in self.text_chunks]

        headers = {
            "Authorization": f"Bearer {self.config.openai_api_key}",
            "Content-Type": "application/json"
        }

        # 分批处理以避免API限制
        batch_size = 100
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]

            data = {
                "input": batch_texts,
                "model": self.config.embedding_model
            }

            try:
                response = requests.post(
                    "https://api.openai.com/v1/embeddings",
                    headers=headers,
                    json=data,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    batch_embeddings = [item["embedding"] for item in result["data"]]
                    all_embeddings.extend(batch_embeddings)
                    print(f"  📊 已处理 {min(i+batch_size, len(texts))}/{len(texts)} 个文本块")
                else:
                    print(f"  ⚠️ API请求失败: {response.status_code}")

            except Exception as e:
                print(f"  ❌ 生成embedding时出错: {e}")

        self.embeddings = np.array(all_embeddings)

    def _generate_local_embeddings(self):
        """使用本地模型生成embeddings"""
        try:
            from sentence_transformers import SentenceTransformer

            print("  🔄 加载本地embedding模型...")
            model = SentenceTransformer(self.config.local_embedding_model)

            texts = [chunk["text"] for chunk in self.text_chunks]
            self.embeddings = model.encode(texts, show_progress_bar=True)

        except Exception as e:
            print(f"❌ 本地embedding生成失败: {e}")

    def save_vector_store(self):
        """保存向量存储"""
        try:
            vector_store_data = {
                "chunks": self.text_chunks,
                "embeddings": self.embeddings,
                "config": self.config.__dict__,
                "timestamp": time.time()
            }

            with open(self.config.vector_store_path, 'wb') as f:
                pickle.dump(vector_store_data, f)

            print(f"💾 向量存储已保存到: {self.config.vector_store_path}")

        except Exception as e:
            print(f"⚠️ 保存向量存储时出错: {e}")

    def load_vector_store(self):
        """加载向量存储"""
        try:
            if os.path.exists(self.config.vector_store_path):
                with open(self.config.vector_store_path, 'rb') as f:
                    data = pickle.load(f)

                self.text_chunks = data["chunks"]
                self.embeddings = data["embeddings"]
                print(f"📂 已加载向量存储: {len(self.text_chunks)} 个文本块")
                return True
        except Exception as e:
            print(f"⚠️ 加载向量存储时出错: {e}")

        return False

    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """智能语义搜索"""
        if not hasattr(self, 'embeddings') or self.embeddings is None:
            return []

        top_k = top_k or self.config.top_k

        # 生成查询的embedding
        query_embedding = self._get_query_embedding(query)
        if query_embedding is None:
            return []

        # 计算相似度
        similarities = self._compute_similarity(query_embedding)

        # 获取top-k结果
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            if similarities[idx] >= self.config.similarity_threshold:
                chunk = self.text_chunks[idx]
                results.append({
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "similarity": float(similarities[idx]),
                    "word_count": chunk["word_count"]
                })

        return results

    def _get_query_embedding(self, query: str) -> np.ndarray:
        """获取查询的embedding"""
        if self.api_available["openai"] and self.config.openai_api_key:
            return self._get_openai_embedding(query)
        elif self.api_available["sentence_transformer"]:
            return self._get_local_embedding(query)
        else:
            return None

    def _get_openai_embedding(self, text: str) -> np.ndarray:
        """使用OpenAI获取embedding"""
        headers = {
            "Authorization": f"Bearer {self.config.openai_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "input": text,
            "model": self.config.embedding_model
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return np.array(result["data"][0]["embedding"])
            else:
                print(f"⚠️ OpenAI API请求失败: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ OpenAI embedding请求失败: {e}")
            return None

    def _get_local_embedding(self, text: str) -> np.ndarray:
        """使用本地模型获取embedding"""
        try:
            from sentence_transformers import SentenceTransformer

            if not hasattr(self, 'local_model'):
                self.local_model = SentenceTransformer(self.config.local_embedding_model)

            return self.local_model.encode(text)

        except Exception as e:
            print(f"❌ 本地embedding请求失败: {e}")
            return None

    def _compute_similarity(self, query_embedding: np.ndarray) -> np.ndarray:
        """计算相似度"""
        # 使用余弦相似度
        similarities = np.dot(self.embeddings, query_embedding)
        norms = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        return similarities / norms

    def generate_response(self, query: str, context: List[Dict]) -> str:
        """生成智能响应"""
        if not context:
            return "抱歉，我在知识库中没有找到相关信息。请尝试使用更具体的关键词。"

        # 构建上下文
        context_text = "\n\n".join([f"[来源: {c['source']}]\n{c['text']}" for c in context[:3]])

        # 使用OpenAI生成响应
        if self.api_available["openai"] and self.config.openai_api_key:
            return self._generate_openai_response(query, context_text)
        else:
            return self._generate_rule_based_response(query, context)

    def _generate_openai_response(self, query: str, context: str) -> str:
        """使用OpenAI生成响应"""
        headers = {
            "Authorization": f"Bearer {self.config.openai_api_key}",
            "Content-Type": "application/json"
        }

        system_prompt = """你是一个专业的生物医学数据分析专家，基于FigureYa知识库回答用户的问题。

请根据提供的上下文信息，专业、准确地回答用户的问题。回答要求：
1. 基于上下文信息，不要编造内容
2. 提供具体的建议和指导
3. 使用中文回答
4. 保持专业但易懂的语气
5. 如果上下文不足，诚实地说明局限性"""

        user_prompt = f"""用户问题：{query}

相关知识库上下文：
{context_text}

请基于以上信息回答用户的问题。"""

        data = {
            "model": self.config.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"⚠️ OpenAI API请求失败: {response.status_code}")
                return self._generate_rule_based_response(query, context)

        except Exception as e:
            print(f"❌ OpenAI请求失败: {e}")
            return self._generate_rule_based_response(query, context)

    def _generate_rule_based_response(self, query: str, context: List[Dict]) -> str:
        """基于规则的响应生成（备选方案）"""
        if not context:
            return "抱歉，我没有找到相关信息。请尝试使用更具体的关键词，比如'RNA-seq差异表达分析'。"

        # 提取最相关的信息
        best_match = context[0]

        response = f"""根据您的查询，我找到了以下相关信息：

📊 **推荐模块**: {best_match['source']}
🎯 **相似度**: {best_match['similarity']:.2f}

**相关内容**:
{best_match['text'][:300]}...

💡 **建议**:
1. 根据上述信息，建议您查看完整的模块文档
2. 如果需要更具体的指导，请提供更多详细信息
3. 考虑结合您的具体数据类型和实验设计

需要我提供更多详细信息吗？"""

        return response

    def chat(self, query: str) -> Dict:
        """智能对话接口"""
        # 搜索相关知识
        search_results = self.search(query)

        # 生成响应
        response = self.generate_response(query, search_results)

        return {
            "query": query,
            "response": response,
            "sources": [r["source"] for r in search_results],
            "confidence": max([r["similarity"] for r in search_results]) if search_results else 0.0,
            "search_results": search_results
        }

    def get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            "status": "ready",
            "apis_available": self.api_available,
            "knowledge_size": len(self.text_chunks),
            "embedding_model": self.config.embedding_model if self.api_available["openai"] else self.config.local_embedding_model,
            "llm_model": self.config.openai_model if self.api_available["openai"] else "rule_based",
            "features": [
                "语义搜索" if self.embeddings is not None else "关键词搜索",
                "LLM生成" if self.api_available["openai"] else "规则生成",
                "上下文理解",
                "智能推荐"
            ]
        }


def main():
    """主函数"""
    print("🧠 FigureYa 智能RAG系统")
    print("=" * 40)

    # 配置API密钥
    config = RAGConfig()
    config.openai_api_key = os.getenv("OPENAI_API_KEY", "")

    if not config.openai_api_key:
        print("⚠️ 未设置OpenAI API密钥")
        print("💡 请设置环境变量: export OPENAI_API_KEY='your-api-key'")
        print("🔄 将使用本地模型和规则生成")

    # 初始化系统
    rag = SmartFigureYaRAG(config)

    # 加载或构建知识库
    if not rag.load_vector_store():
        rag.load_knowledge_base()
        rag.save_vector_store()

    # 显示系统信息
    info = rag.get_system_info()
    print("\n📊 系统信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    # 示例查询
    test_queries = [
        "RNA-seq差异表达分析",
        "生存分析的方法",
        "单细胞质量控制",
        "如何解释火山图"
    ]

    print("\n🔍 测试查询:")
    for query in test_queries:
        print(f"\n❓ 查询: {query}")
        result = rag.chat(query)
        print(f"💬 回答: {result['response'][:100]}...")
        print(f"🎯 置信度: {result['confidence']:.2f}")


if __name__ == "__main__":
    main()