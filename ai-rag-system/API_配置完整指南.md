# 🔑 FigureYa 智能RAG系统 - API配置完整指南

## 🎯 快速开始

### 方法1: 一键配置 (推荐新手)
```bash
# 运行自动配置脚本
python3 quick_setup.py

# 或运行演示配置
python3 setup_and_test.py
```

### 方法2: 手动配置
```bash
# 1. 编辑配置文件
nano .env

# 2. 修改API密钥行
OPENAI_API_KEY=sk-your-actual-key-here

# 3. 保存并运行
source .env && python3 smart_figureya_rag.py
```

## 📍 获取API密钥

### OpenAI API (推荐)
1. **访问**: https://platform.openai.com/api-keys
2. **注册**: 使用邮箱创建账户
3. **充值**: 建议充值 $5-10 USD
4. **创建**: 点击 "Create new secret key"
5. **复制**: 保存密钥 (格式: sk-proj-...)

### 其他API选项
- **Anthropic Claude**: https://console.anthropic.com/
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **本地模型**: Ollama (免费但需要GPU)

## ⚙️ 配置方法详解

### 方法A: .env文件配置 (最推荐)
```bash
# 1. 打开配置文件
open .env

# 2. 找到并修改这行
OPENAI_API_KEY=sk-proj-your-actual-key-here

# 3. 保存文件

# 4. 加载并运行
source .env && python3 smart_figureya_rag.py
```

### 方法B: 环境变量配置
```bash
# 设置环境变量
export OPENAI_API_KEY='sk-proj-your-actual-key-here'

# 验证设置
echo $OPENAI_API_KEY

# 运行系统
python3 smart_figureya_rag.py
```

### 方法C: 命令行传递
```bash
# 一次性运行
OPENAI_API_KEY='sk-proj-your-key' python3 smart_figureya_rag.py

# 或使用Python
OPENAI_API_KEY='sk-proj-your-key' python3 -c "
import os
from smart_figureya_rag import SmartFigureYaRAG, RAGConfig
config = RAGConfig(openai_api_key=os.getenv('OPENAI_API_KEY'))
rag = SmartFigureYaRAG(config)
print('智能RAG系统已就绪!')
"
```

## 🧪 测试API连接

### 简单测试
```bash
python3 -c "
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello'}],
    max_tokens=5
)
print('✅ API连接成功!')
print(f'回复: {response.choices[0].message.content}')
"
```

### 完整功能测试
```bash
# 测试智能演示
python3 demo_smart_rag.py

# 测试完整AI功能 (需要API密钥)
python3 smart_figureya_rag.py

# Web界面测试
python3 figureya_rag_server_fixed.py
```

## 🚀 运行智能RAG系统

### 基础版本 (无需API)
```bash
# 演示版本
python3 demo_smart_rag.py

# 功能测试
python3 test_full_smart_rag.py
```

### 完整AI版本 (需要API密钥)
```bash
# 智能RAG系统
python3 smart_figureya_rag.py

# Web界面
python3 figureya_rag_server_fixed.py

# 服务器启动脚本
./start_figureya_rag.sh
```

## 📊 功能对比

| 特性 | 基础版本 | AI版本 |
|------|----------|--------|
| 搜索方式 | 关键词匹配 | 语义向量搜索 |
| 回答质量 | 模板化回答 | GPT智能生成 |
| 理解能力 | 简单模式匹配 | 上下文理解 |
| 置信度 | 0.65-0.75 | 0.85-0.95 |
| 个性化 | 低 | 高 |
| 依赖 | 无需API | 需要OpenAI API |

## 🔧 配置文件说明

### .env文件示例
```bash
# FigureYa 智能RAG系统 API配置

# OpenAI API (主要)
OPENAI_API_KEY=sk-proj-your-actual-key-here

# 可选配置
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
CHUNK_SIZE=500
TOP_K=5

# 其他API (可选)
ANTHROPIC_API_KEY=your-anthropic-key
GEMINI_API_KEY=your-gemini-key
```

### 高级配置选项
```python
from smart_figureya_rag import SmartFigureYaRAG, RAGConfig

# 自定义配置
config = RAGConfig(
    openai_api_key="your-key",
    openai_model="gpt-4",  # 更强大的模型
    embedding_model="text-embedding-3-large",  # 更好的embedding
    chunk_size=1000,  # 更大的文本块
    top_k=10,  # 更多搜索结果
    similarity_threshold=0.8  # 更高的相似度阈值
)

rag = SmartFigureYaRAG(config)
```

## 💡 使用建议

### 新手用户
1. 先运行 `python3 demo_smart_rag.py` 体验基础功能
2. 获取OpenAI API密钥
3. 使用 `python3 quick_setup.py` 一键配置
4. 体验完整AI功能

### 高级用户
1. 编辑 `.env` 文件进行详细配置
2. 可以使用更强大的GPT-4模型
3. 调整参数优化性能
4. 集成到自己的项目中

### 开发者
1. 查看源码了解实现原理
2. 修改配置适配自己的需求
3. 扩展功能模块
4. 部署到服务器

## 🛠️ 故障排除

### 常见问题
1. **API密钥无效**: 检查密钥格式和余额
2. **网络连接问题**: 确保能访问OpenAI服务
3. **包安装失败**: 使用 `pip install --upgrade pip`
4. **权限问题**: 使用 `chmod +x *.sh`

### 调试方法
```bash
# 检查配置
cat .env

# 检查API密钥
echo $OPENAI_API_KEY

# 测试网络
curl -I https://api.openai.com

# 查看日志
python3 smart_figureya_rag.py 2>&1 | tee rag.log
```

## 📈 成本估算

### OpenAI API费用 (GPT-3.5-turbo)
- **输入**: $0.001 per 1K tokens
- **输出**: $0.002 per 1K tokens
- **Embedding**: $0.0001 per 1K tokens

### 预估使用量
- **轻度使用**: $1-5/月
- **中度使用**: $5-20/月
- **重度使用**: $20-50/月

## 🔗 相关资源

### 官方文档
- [OpenAI API文档](https://platform.openai.com/docs)
- [FigureYa项目主页](https://github.com/example/figureya)
- [RAG系统架构](https://example.com/rag-guide)

### 工具文件
- `quick_setup.py` - 一键配置工具
- `configure_api.sh` - API配置脚本
- `api_setup_guide.html` - 网页版配置指南
- `demo_smart_rag.py` - 智能演示系统

---

**🎉 配置完成后，您将拥有一个真正智能的生物医学分析助手！**