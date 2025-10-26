# ⚡ 快速API配置指南

## 🎯 3步配置真实API密钥

### 步骤1: 获取API密钥
**访问**: https://platform.openai.com/api-keys
1. 登录/注册OpenAI账户
2. 充值 $5-10 (PayPal/信用卡)
3. 点击 "Create new secret key"
4. 复制密钥 (格式: sk-proj-xxxxxxxxxxx)

### 步骤2: 配置密钥
**选择一种方法**:

#### 方法A: 使用配置脚本 (推荐)
```bash
python3 simple_config.py
# 按提示输入您的API密钥
```

#### 方法B: 手动编辑
```bash
# 1. 打开文件
open .env

# 2. 找到第7行，将:
OPENAI_API_KEY=demo-key-for-testing
# 改为:
OPENAI_API_KEY=sk-proj-您的真实密钥

# 3. 保存文件 (Command+S)
```

#### 方法C: 终端命令
```bash
# 直接替换 (将 sk-proj-xxx 替换为您的密钥)
sed -i '' 's/OPENAI_API_KEY=.*/OPENAI_API_KEY=sk-proj-your-actual-key-here/' .env
```

### 步骤3: 测试并运行
```bash
# 测试配置
source .env && python3 smart_figureya_rag.py
```

## ✅ 配置成功标志

看到以下输出表示配置成功:
```
🧠 FigureYa 智能RAG系统
========================================
✅ OpenAI API已连接
🤖 GPT-3.5智能功能已启用
📊 置信度: 0.85-0.95
```

## 🔥 您将体验的AI功能

- **语义搜索**: 理解查询意图，不是关键词匹配
- **专业回答**: GPT生成的生物医学专家级建议
- **个性化**: 根据您的具体需求定制回答
- **高置信度**: 0.85-0.95的准确度
- **上下文理解**: 能够理解复杂的生物医学问题

## 💡 测试问题示例

配置完成后，可以问这些问题:
- "RNA-seq差异表达分析的最佳方法是什么？"
- "如何解释生存分析的结果？"
- "单细胞数据质控的关键指标有哪些？"
- "PCA分析结果如何专业解读？"

## 🆘 故障排除

**API密钥错误**:
```
❌ 检查密钥格式: sk-proj-xxxxxxxxxxx
❌ 确保没有多余空格
❌ 确认账户有余额
```

**网络问题**:
```
❌ 检查网络连接
❌ 确保能访问 openai.com
❌ 尝试使用VPN
```

---

**🚀 准备好体验真正的AI智能功能了吗？**