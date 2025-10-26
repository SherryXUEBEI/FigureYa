# 🧠 FigureYa AI RAG系统

这是基于智谱AI GLM-4模型的FigureYa智能RAG系统，为生物医学数据分析提供专业的AI驱动建议。

## 📁 文件结构

```
ai-rag-system/
├── README.md                           # 本文件
├── .env.example                        # API密钥配置模板
├── 🤖 核心系统
│   ├── smart_figureya_rag.py          # OpenAI GPT版本
│   ├── zhipuai_rag_system.py          # 智谱AI版本
│   └── demo_smart_rag.py              # 基础演示版本
├── ⚙️ 配置工具
│   ├── quick_setup.py                 # 快速配置
│   ├── interactive_api_setup.py       # 交互式配置
│   ├── simple_config.py               # 简单配置
│   ├── quick_zhipuai_setup.py         # 智谱AI快速配置
│   └── zhipuai_config.py              # 智谱AI完整配置
├── 🌐 Web界面
│   ├── figureya_ai_search.html        # AI搜索界面
│   ├── figureya_ai_search_public.html # 公开演示版本
│   └── github_pages_rag_backend.py    # GitHub Pages后端
├── 🧪 测试工具
│   ├── test_full_smart_rag.py         # 完整功能测试
│   └── setup_and_test.py              # 配置测试工具
└── 📚 文档
    ├── API_配置完整指南.md             # 详细配置指南
    ├── QUICK_API_CONFIG.md             # 快速配置指南
    ├── real_api_config_guide.md        # 真实API配置
    ├── GitHub_Pages_AI_集成指南.md     # GitHub Pages集成
    └── 隐私安全指南.md                  # 隐私安全指南
```

## 🚀 快速开始

### 方法1: 使用智谱AI（推荐）
```bash
# 1. 配置智谱AI API密钥
python3 quick_zhipuai_setup.py

# 2. 运行智谱AI RAG系统
export ZHIPUAI_API_KEY="your-key-here"
python3 zhipuai_rag_system.py
```

### 方法2: 使用OpenAI API
```bash
# 1. 配置OpenAI API密钥
python3 quick_setup.py

# 2. 运行OpenAI RAG系统
export OPENAI_API_KEY="your-key-here"
python3 smart_figureya_rag.py
```

### 方法3: 基础演示（无需API）
```bash
python3 demo_smart_rag.py
```

## 🌐 Web界面使用

### 本地Web界面
```bash
# 启动Web服务器
python3 github_pages_rag_backend.py --mock --port 8080

# 访问地址
open http://localhost:8080
```

### GitHub Pages部署
```bash
# 提交安全版本到GitHub
git add ai-rag-system/figureya_ai_search_public.html
git commit -m "Add AI search demo for GitHub Pages"
git push origin main

# 访问地址
https://ying-ge.github.io/FigureYa/ai-rag-system/figureya_ai_search_public.html
```

## 🔑 API密钥配置

### 智谱AI
```bash
# 获取地址: https://bigmodel.cn/usercenter/proj-mgmt/apikeys
export ZHIPUAI_API_KEY="your-zhipuai-key"
```

### OpenAI
```bash
# 获取地址: https://platform.openai.com/api-keys
export OPENAI_API_KEY="your-openai-key"
```

## 📊 功能对比

| 功能 | 基础版本 | 智谱AI版本 | OpenAI版本 |
|------|----------|------------|------------|
| **搜索方式** | 关键词匹配 | 语义搜索 | 语义搜索 |
| **回答质量** | 模板化 | GLM-4专业 | GPT-3.5专业 |
| **中文支持** | 基础 | 优秀 | 良好 |
| **成本** | 免费 | 付费 | 付费 |
| **部署** | 简单 | 中等 | 中等 |

## 🎯 使用场景

### 1. 模块推荐
- RNA-seq差异表达分析
- 生存分析和预后评估
- 单细胞RNA测序分析
- PCA主成分分析

### 2. 参数指导
- 统计阈值设置
- 质量控制标准
- 数据预处理流程

### 3. 结果解读
- 图表专业解读
- 生物学意义分析
- 后续分析建议

## 🔒 隐私安全

- ✅ API密钥已添加到 `.gitignore`
- ✅ 提供安全的公开演示版本
- ✅ 详细的安全配置指南
- ✅ 支持环境变量配置

## 📞 技术支持

### 配置问题
1. 查看 `API_配置完整指南.md`
2. 运行 `python3 quick_setup.py`
3. 检查API密钥格式

### 功能问题
1. 运行基础测试：`python3 demo_smart_rag.py`
2. 查看完整测试：`python3 test_full_smart_rag.py`
3. 检查网络连接

### 部署问题
1. 查看 `GitHub_Pages_AI_集成指南.md`
2. 使用安全版本：`figureya_ai_search_public.html`
3. 检查隐私安全配置

## 🎉 开始体验

1. **选择模型**: 智谱AI 或 OpenAI
2. **配置API**: 运行相应的配置脚本
3. **启动系统**: 运行对应的Python脚本
4. **开始提问**: 输入您的生物医学分析问题

**🚀 现在就开始使用AI驱动的生物医学分析助手吧！**