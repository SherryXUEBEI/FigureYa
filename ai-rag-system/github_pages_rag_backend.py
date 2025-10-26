#!/usr/bin/env python3
"""
GitHub Pages兼容的智谱AI RAG后端服务
可以通过GitHub Actions部署，提供AI搜索API
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from dataclasses import dataclass
import subprocess

# 模拟智谱AI SDK (如果在GitHub Pages环境中可能无法安装真实SDK)
class MockZhipuAI:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def chat(self, messages: List[Dict], **kwargs):
        """模拟聊天完成"""
        # 模拟API延迟
        import time
        time.sleep(1)

        # 获取用户消息
        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        # 生成模拟回复
        response_text = self._generate_mock_response(user_message)

        return MockCompletion(response_text)

    def _generate_mock_response(self, query: str) -> str:
        """生成模拟回复"""
        responses = {
            "RNA-seq": """基于您的查询，我推荐使用**FigureYa59volcanoV2**模块进行RNA-seq差异表达分析。

🎯 **推荐理由**：
• 火山图是最直观的差异表达基因可视化方法
• 能够同时展示统计显著性和生物学意义
• 支持DESeq2、edgeR、limma等多种分析方法

📊 **分析步骤**：
1. 数据预处理和质量控制
2. 使用DESeq2进行差异表达分析
3. 设置合适的阈值（pvalue < 0.05, |logFC| > 1）
4. 生成火山图进行结果可视化

💡 **参数建议**：
• pvalue阈值：0.05（统计学显著性）
• logFC阈值：1.0（生物学意义，2倍变化）
• 建议结合功能富集分析进行深度解读""",

            "生存分析": """对于生存分析，我推荐使用**FigureYa36nSurvV3**模块。

🔬 **方法选择**：
• **Kaplan-Meier法**：适用于生存曲线估计和比较
• **Cox回归模型**：用于多因素预后分析

📈 **分析要点**：
1. 数据准备：生存时间、事件状态、协变量
2. 生存曲线绘制：Kaplan-Meier法
3. 统计检验：Log-rank检验比较组间差异
4. 风险评估：计算风险比(HR)和置信区间

⚠️ **注意事项**：
• 确保足够的事件数量（建议每组≥10个事件）
• 检查比例风险假设
• 考虑混杂因素的影响""",

            "单细胞": """单细胞RNA测序分析是一个复杂的多步骤流程，推荐使用**FigureYa274MuSiCbulkProop**模块。

🔍 **完整分析流程**：

1. **数据质控**
   • 细胞过滤：排除低质量细胞
   • 基因过滤：排除低表达基因
   • 双细胞检测和移除

2. **标准化和归一化**
   • 计算标准化表达值
   • 批次效应校正

3. **特征选择和降维**
   • 高变基因识别
   • PCA降维分析
   • UMAP/tSNE可视化

4. **聚类分析**
   • 细胞类型识别
   • 亚群分析

5. **差异表达分析**
   • 簷群间差异基因识别
   • 标记基因筛选

💡 **质控关键指标**：
• 每个细胞检测到的基因数（200-6000为佳）
• 线粒体基因比例（<10-15%）
• rRNA比例（<5%）""",

            "PCA": """对于PCA分析，我推荐使用**FigureYa38PCA**模块。

📊 **PCA分析要点**：

1. **数据准备**
   • 标准化数据（z-score标准化）
   • 处理缺失值
   • 检查异常值

2. **主成分选择**
   • 查看方差解释比例
   • 使用肘部法则确定主成分数量
   • 通常保留解释85%以上方差的主成分

3. **结果解读**
   • PC1和PC2通常解释大部分变异
   • 样本在主成分空间中的分布反映相似性
   • 载荷矩阵显示变量的贡献度

4. **可视化**
   • 散点图展示样本关系
   • 载荷图展示变量重要性
   • 碎石图显示主成分重要性

🔍 **应用场景**：
• 数据降维和可视化
• 异常值检测
• 样本聚类分析"""
        }

        # 根据查询内容返回相应回答
        for key, response in responses.items():
            if key.lower() in query.lower():
                return response

        # 默认回答
        return f"""基于您的查询"{query}"，我建议您：

1. **明确分析目标**：确定您想要解决的具体生物学问题
2. **选择合适模块**：根据数据类型选择相应的FigureYa模块
3. **数据准备**：确保数据格式符合要求，进行必要的数据清洗
4. **参数设置**：根据统计学原理和生物学意义设置合适的参数阈值
5. **结果验证**：使用多种方法交叉验证分析结果的可靠性

💡 如果您能提供更具体的信息（如数据类型、研究目标等），我可以为您提供更精准的建议。

🔍 **推荐的通用模块**：
• **FigureYa59volcanoV2**：差异表达分析
• **FigureYa38PCA**：数据降维和可视化
• **FigureYa36nSurvV3**：生存分析
• **FigureYa274MuSiCbulkProop**：单细胞分析"""

class MockCompletion:
    def __init__(self, content: str):
        self.choices = [MockChoice(content)]

class MockChoice:
    def __init__(self, content: str):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content: str):
        self.content = content

# 尝试导入真实的智谱AI SDK
try:
    from zhipuai import ZhipuAI as RealZhipuAI
    ZhipuAI_AVAILABLE = True
except ImportError:
    ZhipuAI_AVAILABLE = False
    ZhipuAI = MockZhipuAI

@dataclass
class RAGConfig:
    """RAG配置"""
    api_key: str = ""
    model: str = "glm-4-flash"
    use_mock: bool = not ZhipuAI_AVAILABLE

class FigureYaRAG:
    """FigureYa RAG系统"""

    def __init__(self, config: RAGConfig):
        self.config = config
        self.knowledge_base = self._build_knowledge_base()

        # 初始化AI客户端
        if config.use_mock:
            self.client = MockZhipuAI(config.api_key)
        else:
            try:
                self.client = RealZhipuAI(api_key=config.api_key)
            except Exception as e:
                print(f"⚠️ 无法初始化智谱AI: {e}")
                self.client = MockZhipuAI(config.api_key)

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
        try:
            # 检索相关知识
            relevant_info = self._retrieve_knowledge(query)

            # 生成智能回答
            response = self._generate_ai_response(query, relevant_info)

            return {
                "query": query,
                "response": response,
                "sources": [info.get("modules", []) for info in relevant_info],
                "model": self.config.model,
                "ai_enhanced": True,
                "use_mock": self.config.use_mock
            }

        except Exception as e:
            return {
                "query": query,
                "response": f"抱歉，处理您的请求时出现错误: {str(e)}",
                "sources": [],
                "model": self.config.model,
                "ai_enhanced": False,
                "error": str(e)
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

    def _generate_ai_response(self, query: str, relevant_info: List[dict]) -> str:
        """使用AI生成回答"""
        try:
            messages = [
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
                    "content": query
                }
            ]

            # 如果是真实API
            if not self.config.use_mock:
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    max_tokens=800,
                    temperature=0.7
                )
                return response.choices[0].message.content
            else:
                # 使用模拟API
                return self.client.chat(messages).choices[0].message.content

        except Exception as e:
            print(f"⚠️ AI API调用失败: {e}")
            return self._fallback_response(query, relevant_info)

    def _fallback_response(self, query: str, relevant_info: List[dict]) -> str:
        """备用回答"""
        if relevant_info:
            best = relevant_info[0]
            return f"""基于您的查询，我推荐以下模块：

🎯 **推荐模块**: {', '.join(best['modules'])}
📝 **功能描述**: {best['description']}
🔬 **技术方法**: {', '.join(best['methods'])}

💡 这是一个基础的推荐结果。如需更专业的个性化建议，建议配置智谱AI API密钥。"""

        return "抱歉，我没有找到相关信息。请尝试使用更具体的关键词。"

class RAGAPIHandler(BaseHTTPRequestHandler):
    """RAG API处理器"""

    def __init__(self, *args, rag_system=None, **kwargs):
        self.rag_system = rag_system
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('figureya_ai_search.html')
        elif self.path == '/api/status':
            self.handle_status()
        elif self.path.startswith('/api/search'):
            self.handle_search()
        else:
            self.serve_static_file(self.path[1:])

    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/chat':
            self.handle_chat()
        else:
            self.send_error(404)

    def handle_status(self):
        """处理状态查询"""
        try:
            status_data = {
                "status": "ready",
                "service": "FigureYa AI RAG",
                "version": "1.0.0",
                "model": "GLM-4-Flash",
                "features": [
                    "智能搜索",
                    "专业分析建议",
                    "模块推荐",
                    "参数指导"
                ],
                "knowledge_base_size": len(self.rag_system.knowledge_base) if self.rag_system else 0,
                "use_mock": self.rag_system.config.use_mock if self.rag_system else True
            }
            self.send_json_response(status_data)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def handle_search(self):
        """处理搜索请求"""
        try:
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            query = query_params.get('q', [''])[0]

            if not query.strip():
                self.send_json_response({"error": "Empty query"}, 400)
                return

            if not self.rag_system:
                self.send_json_response({"error": "RAG system not initialized"}, 503)
                return

            result = self.rag_system.intelligent_search(query)
            self.send_json_response(result)

        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def handle_chat(self):
        """处理聊天请求"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_json_response({"error": "No data received"}, 400)
                return

            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            query = data.get('message', '').strip()

            if not query:
                self.send_json_response({"error": "Empty message"}, 400)
                return

            if not self.rag_system:
                self.send_json_response({"error": "RAG system not initialized"}, 503)
                return

            result = self.rag_system.intelligent_search(query)
            self.send_json_response(result)

        except json.JSONDecodeError:
            self.send_json_response({"error": "Invalid JSON"}, 400)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def serve_file(self, filename):
        """提供文件服务"""
        try:
            file_path = Path(__file__).parent / filename
            if not file_path.exists():
                self.send_error(404)
                return

            with open(file_path, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-type', self.get_content_type(filename))
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            self.send_error(500)

    def serve_static_file(self, filename):
        """提供静态文件服务"""
        try:
            file_path = Path(__file__).parent / filename
            if not file_path.exists():
                self.send_error(404)
                return

            with open(file_path, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-type', self.get_content_type(filename))
            self.send_header('Cache-Control', 'public, max-age=3600')
            self.end_headers()
            self.wfile.write(content)

        except Exception:
            self.send_error(404)

    def send_json_response(self, data, status=200):
        """发送JSON响应"""
        try:
            response_json = json.dumps(data, ensure_ascii=False, indent=2)
            self.send_response(status)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))
        except Exception as e:
            print(f"Error sending JSON response: {e}")

    def get_content_type(self, filename):
        """获取文件内容类型"""
        content_types = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml'
        }

        ext = Path(filename).suffix.lower()
        return content_types.get(ext, 'application/octet-stream')

    def log_message(self, format, *args):
        """减少日志输出"""
        pass

def create_handler_class(rag_system):
    """创建处理器类"""
    class Handler(RAGAPIHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, rag_system=rag_system, **kwargs)
    return Handler

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='FigureYa AI RAG Server')
    parser.add_argument('--host', default='localhost', help='服务器地址')
    parser.add_argument('--port', type=int, default=8080, help='服务器端口')
    parser.add_argument('--api-key', help='智谱AI API密钥')
    parser.add_argument('--mock', action='store_true', help='使用模拟API')

    args = parser.parse_args()

    print("🧠 FigureYa AI RAG 服务器")
    print("=" * 40)

    # 加载API密钥
    api_key = args.api_key or os.getenv("ZHIPUAI_API_KEY")
    if not api_key and not args.mock:
        print("⚠️ 未找到智谱AI API密钥")
        print("💡 使用模拟API模式")
        api_key = "mock-key"

    # 初始化配置
    config = RAGConfig(
        api_key=api_key,
        use_mock=args.mock or (not api_key or api_key == "mock-key")
    )

    # 初始化RAG系统
    rag_system = FigureYaRAG(config)

    print(f"🤖 AI模型: {config.model}")
    print(f"🔧 模拟模式: {'是' if config.use_mock else '否'}")
    print(f"📚 知识库大小: {len(rag_system.knowledge_base)} 个主题")

    # 创建HTTP服务器
    handler_class = create_handler_class(rag_system)
    server = HTTPServer((args.host, args.port), handler_class)

    print(f"🚀 服务器启动成功!")
    print(f"🌐 访问地址: http://{args.host}:{args.port}")
    print(f"📊 API状态: http://{args.host}:{args.port}/api/status")
    print(f"🔍 搜索API: http://{args.host}:{args.port}/api/search?q=RNA-seq")
    print("🛑 按 Ctrl+C 停止服务器")
    print("-" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")

if __name__ == "__main__":
    main()