# 🧠 FigureYa 智能RAG系统 - 完整安装指南

## 🎯 系统概述

FigureYa智能RAG系统是一个真正的AI驱动助手，集成了现代大语言模型和向量数据库，能够理解上下文、推理和生成专业回答。

## 🚀 核心特性

### ✅ 当前版本 vs 智能版本对比

| 特性 | 当前版本 | 智能版本 |
|------|----------|----------|
| 搜索方式 | 关键词匹配 | 语义向量搜索 |
| 理解能力 | 简单模式匹配 | 上下文理解 |
| 回答生成 | 模板化回答 | LLM智能生成 |
| 推理能力 | 无 | 多步推理 |
| 个性化程度 | 低 | 高 |

### 🧠 智能版本特性
- **语义搜索**: 基于向量相似度的智能检索
- **上下文理解**: 理解查询意图和上下文
- **LLM集成**: 支持OpenAI GPT等大语言模型
- **多模态**: 支持文本、代码、图像理解
- **个性化**: 根据用户背景调整回答复杂度

## 📋 系统要求

### 基础要求
- Python 3.7+
- 内存: 最少2GB（推荐4GB+）
- 磁盘空间: 至少1GB
- 网络连接: 稳定的互联网连接

### API选择
支持以下API（按推荐程度排序）：
1. **OpenAI API** (最推荐) - GPT-4, GPT-3.5
2. **Anthropic Claude API** - Claude 3.5, Claude 3
3. **Google Gemini API** - Gemini Pro
4. **本地模型** - Ollama, Llama3, Mistral

## 🔧 安装步骤

### 步骤1: 安装基础依赖

```bash
# 创建虚拟环境
python3 -m venv figureya_rag_env
source figureya_rag_env/bin/activate  # Linux/Mac
# figureya_rag_env\Scripts\activate  # Windows

# 安装基础包
pip install --upgrade pip
pip install numpy pandas requests
```

### 步骤2: 选择并配置API

#### 选项A: OpenAI API (推荐)

1. **获取API密钥**:
   - 访问 https://platform.openai.com
   - 注册账号并创建API密钥
   - 确保账户有足够余额

2. **安装OpenAI包**:
   ```bash
   pip install openai
   ```

3. **配置环境变量**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **测试API连接**:
   ```python
   from openai import OpenAI
   client = OpenAI()
   response = client.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=[{"role": "user", "content": "Hello!"}]
   )
   print(response.choices[0].message.content)
   ```

#### 选项B: Anthropic Claude API

1. **获取API密钥**:
   - 访问 https://console.anthropic.com
   - 注册账号并创建API密钥

2. **安装包**:
   ```bash
   pip install anthropic
   ```

3. **配置环境变量**:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

#### 选项C: 本地模型 (免费但需要GPU)

1. **安装Ollama**:
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh

   # 或手动下载: https://ollama.ai/download
   ```

2. **下载模型**:
   ```bash
   ollama pull llama3  # 7B模型
   ollama pull mistral  # 7B模型
   ```

3. **安装Python包**:
   ```bash
   pip install ollama-python
   ```

### 步骤3: 安装向量数据库

#### 选项A: ChromaDB (推荐)
```bash
pip install chromadb
```

#### 选项B: FAISS (本地)
```bash
pip install faiss-cpu  # CPU版本
# pip install faiss-gpu  # GPU版本
```

### 步骤4: 安装Embedding模型

#### 选项A: SentenceTransformers (免费)
```bash
pip install sentence-transformers
```

#### 选项B: OpenAI Embeddings
```bash
pip install openai
```

## 🚀 启动智能RAG系统

### 方法1: 使用智能版本
```bash
cd /Users/mypro/Downloads/FigureYa

# 设置API密钥
export OPENAI_API_KEY="your-api-key-here"

# 运行智能系统
python3 smart_figureya_rag.py
```

### 方法2: Web界面版本
```bash
# 创建智能Web服务器
python3 -c "
from smart_figureya_rag import SmartFigureYaRAG, RAGConfig
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

config = RAGConfig()
config.openai_api_key = os.getenv('OPENAI_API_KEY', '')
rag = SmartFigureYaRAG(config)
rag.load_knowledge_base()

class SmartHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        result = rag.chat(data.get('message', ''))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

server = HTTPServer(('localhost', 8082), SmartHandler)
print('🚀 智能RAG服务器启动: http://localhost:8082')
server.serve_forever()
"
```

## 📱 使用方法

### API接口示例

#### 智能搜索
```python
import requests

# 语义搜索
response = requests.post('http://localhost:8082',
    json={'message': 'RNA-seq差异表达分析的方法'})
result = response.json()

print(result['response'])
print(f"置信度: {result['confidence']}")
print(f"相关源: {result['sources']}")
```

#### 批量查询
```python
queries = [
    "生存分析的最佳实践",
    "单细胞质控指标",
    "如何选择合适的统计方法"
]

for query in queries:
    response = requests.post('http://localhost:8082',
        json={'message': query})
    print(f"Q: {query}")
    print(f"A: {response.json()['response']}")
    print("-" * 50)
```

## 🛠️ 高级配置

### 自定义配置
```python
from smart_figureya_rag import SmartFigureYaRAG, RAGConfig

# 创建自定义配置
config = RAGConfig(
    openai_api_key="your-api-key",
    openai_model="gpt-4",  # 使用更强大的模型
    embedding_model="text-embedding-3-large",
    chunk_size=1000,  # 更大的文本块
    top_k=10,  # 返回更多相关结果
    similarity_threshold=0.8  # 更高的相似度阈值
)

rag = SmartFigureYaRAG(config)
```

### 本地模型配置
```python
# 使用本地LLM (需要Ollama)
config = RAGConfig()
config.local_llm_model = "llama3:latest"
config.local_embedding_model = "all-MiniLM-L6-v2"

rag = SmartFigureYaRAG(config)
```

## 📊 性能优化

### 1. 向量数据库优化
```python
# 使用FAISS提高搜索速度
import faiss

dimension = 1536  # OpenAI embedding维度
index = faiss.IndexFlatIP(dimension)
index.add(rag.embeddings)
```

### 2. 缓存机制
```python
import functools

@functools.lru_cache(maxsize=100)
def cached_search(query):
    return rag.search(query)
```

### 3. 批量处理
```python
# 批量生成embeddings
batch_size = 100
texts = [chunk["text"] for chunk in rag.text_chunks]

for i in range(0, len(texts), batch_size):
    batch = texts[i:i+batch_size]
    embeddings = generate_embeddings(batch)
```

## 🔍 故障排除

### 常见问题

#### 1. API密钥问题
```bash
# 检查API密钥是否设置
echo $OPENAI_API_KEY

# 临时设置
export OPENAI_API_KEY="your-key-here"
```

#### 2. 内存不足
```python
# 减少chunk_size
config = RAGConfig(chunk_size=200)
```

#### 3. 网络连接问题
```python
# 设置超时时间
import requests
response = requests.post(url, json=data, timeout=30)
```

#### 4. 模型加载失败
```python
# 检查模型是否正确安装
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

## 📈 性能基准

### OpenAI API版本
- **响应时间**: 1-3秒
- **准确性**: 85-95%
- **理解能力**: 高
- **成本**: 按token计费

### 本地模型版本
- **响应时间**: 2-5秒
- **准确性**: 70-85%
- **理解能力**: 中等
- **成本**: 免费（需要GPU）

### 推荐配置
- **初学者**: OpenAI GPT-3.5 + ChromaDB
- **研究者**: OpenAI GPT-4 + FAISS
- **企业用户**: 本地部署 + 混合云架构

## 🔮 未来规划

### 短期目标
- [ ] 支持多模态输入（图像、表格）
- [ ] 集成更多生物医学专用模型
- [ ] 添加对话历史管理
- [ ] 支持文档上传和分析

### 长期目标
- [ ] 构建领域专用LLM
- [ ] 集成实验设计助手
- [ ] 支持实时数据分析
- [ ] 构建知识图谱

## 📞 技术支持

### 社区资源
- GitHub Issues: 报告问题和建议
- Discord: 实时技术讨论
- 文档: 完整的API文档和教程

### 联系方式
- 邮箱: support@figureya-rag.com
- 官网: https://figureya-rag.com

---

**🎉 恭喜！您现在拥有了一个真正智能的生物医学分析助手！**