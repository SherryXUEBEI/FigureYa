# 🧠 FigureYa AI RAG系统

基于智谱AI GLM-4和OpenAI GPT的智能生物医学数据分析助手，为FigureYa 300+ 模块提供专业AI驱动的搜索和建议功能。

## 📁 文件组织

所有AI RAG相关文件已整理到 `ai-rag-system/` 目录中：

```
ai-rag-system/
├── 🤖 核心系统
│   ├── zhipuai_rag_system.py          # 智谱AI版本 (推荐)
│   ├── smart_figureya_rag.py          # OpenAI GPT版本
│   └── demo_smart_rag.py              # 基础演示版本
├── ⚙️ 配置工具
│   ├── quick_zhipuai_setup.py         # 智谱AI一键配置
│   ├── quick_setup.py                 # OpenAI一键配置
│   └── quick_start.sh                 # 快速启动脚本
├── 🌐 Web界面
│   ├── figureya_ai_search_public.html # 安全演示版本 ⭐
│   ├── figureya_ai_search.html        # 完整功能版本
│   └── github_pages_rag_backend.py    # Web后端服务
└── 📚 完整文档
    ├── README.md                       # 系统使用指南
    ├── API_配置完整指南.md             # 详细配置说明
    ├── GitHub_Pages_AI_集成指南.md     # 部署指南
    └── 隐私安全指南.md                  # 安全配置
```

## 🚀 快速开始

### 方法1: 一键启动（推荐）
```bash
cd ai-rag-system
./quick_start.sh
```

### 方法2: 智谱AI版本
```bash
cd ai-rag-system
python3 quick_zhipuai_setup.py  # 配置API密钥
python3 zhipuai_rag_system.py   # 启动系统
```

### 方法3: 基础演示（无需API）
```bash
cd ai-rag-system
python3 demo_smart_rag.py
```

### 方法4: Web界面
```bash
cd ai-rag-system
open figureya_ai_search_public.html
```

## 🌐 在线演示

### GitHub Pages部署地址
```
https://ying-ge.github.io/FigureYa/ai-rag/
```

**注意**: 这是安全的演示版本，使用模拟数据，无需API密钥。

## 🔑 API密钥配置

### 智谱AI（推荐）
1. 访问: https://bigmodel.cn/usercenter/proj-mgmt/apikeys
2. 创建API密钥
3. 运行配置脚本: `python3 quick_zhipuai_setup.py`

### OpenAI
1. 访问: https://platform.openai.com/api-keys
2. 创建API密钥
3. 运行配置脚本: `python3 quick_setup.py`

## 📊 功能特点

### 🧠 智能理解
- 理解复杂的生物医学问题
- 语义搜索而非关键词匹配
- 上下文相关的回答生成

### 🔬 专业建议
- 基于GLM-4/GPT的专业分析建议
- FigureYa模块智能推荐
- 参数设置和质控指导

### 🎯 个性化推荐
- 根据数据类型推荐分析方法
- 提供具体的分析流程
- 结果解读和后续建议

## 🎯 支持的分析类型

1. **RNA-seq差异表达分析**
   - DESeq2、edgeR、limma方法比较
   - 火山图和热图可视化
   - 差异基因筛选标准

2. **生存分析**
   - Kaplan-Meier生存曲线
   - Cox回归模型
   - 风险比计算和解读

3. **单细胞RNA测序**
   - 数据质控和预处理
   - 聚类分析和细胞类型识别
   - 差异表达分析

4. **PCA主成分分析**
   - 数据降维和可视化
   - 主成分选择和解释
   - 异常值检测

## 🔒 隐私安全

- ✅ 所有API密钥已添加到 `.gitignore`
- ✅ 提供完全安全的公开演示版本
- ✅ 详细的安全配置指南
- ✅ 支持环境变量和GitHub Secrets

## 📋 使用场景

### 科研人员
- 快速了解适合的分析方法
- 获得专业的参数设置建议
- 理解复杂分析结果的含义

### 生物信息学家
- 选择合适的统计工具
- 优化数据分析流程
- 验证分析结果的可靠性

### 临床研究者
- 选择合适的生存分析方法
- 理解预后分析的统计指标
- 获得临床意义的解读建议

## 🛠️ 技术架构

```
用户查询 → 智能意图识别 → 知识库检索 → AI模型生成 → 专业回答
```

### 前端技术
- HTML5 + CSS3 + JavaScript
- 响应式设计，支持移动端
- 现代化UI/UX设计

### 后端技术
- Python + 智谱AI SDK
- OpenAI GPT API集成
- RESTful API接口

### AI模型
- 智谱AI GLM-4-Flash（中文优化）
- OpenAI GPT-3.5-turbo（英文优化）
- 支持模型切换和比较

## 📞 技术支持

### 配置问题
1. 查看 `ai-rag-system/API_配置完整指南.md`
2. 运行快速配置脚本
3. 检查API密钥格式和网络连接

### 功能问题
1. 尝试基础演示版本
2. 检查Python环境和依赖
3. 查看详细错误日志

### 部署问题
1. 参考 `ai-rag-system/GitHub_Pages_AI_集成指南.md`
2. 使用安全的演示版本
3. 检查GitHub Actions配置

## 🎉 开始使用

1. **访问演示**: 打开在线演示版本体验功能
2. **配置API**: 获取并配置您的API密钥
3. **本地使用**: 运行完整版本获得最佳体验
4. **自定义**: 根据需求修改和扩展功能

---

**🎊 现在就开始使用AI驱动的生物医学分析助手吧！**