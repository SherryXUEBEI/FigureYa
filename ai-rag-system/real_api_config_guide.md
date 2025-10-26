# 🔑 配置真实OpenAI API密钥 - 详细步骤

## 📋 准备工作

### 1. 获取OpenAI API密钥
1. **访问**: https://platform.openai.com/api-keys
2. **登录/注册**: 使用您的Google或邮箱账户
3. **充值**: 建议充值 $5-10 USD (PayPal或信用卡)
4. **创建密钥**:
   - 点击 "Create new secret key"
   - 命名为 "FigureYa-RAG"
   - 复制密钥 (格式: sk-proj-xxxxxxxxxxx)

### 2. API密钥格式示例
```
sk-proj-abcd1234efgh5678ijkl9012mnop3456
```

## ⚙️ 配置方法

### 方法A: 编辑.env文件 (推荐)
```bash
# 1. 打开配置文件
open .env

# 2. 找到第7行，将 demo-key-for-testing 替换为您的真实密钥
# 改前: OPENAI_API_KEY=demo-key-for-testing
# 改后: OPENAI_API_KEY=sk-proj-your-actual-key-here

# 3. 保存文件 (Command+S)
```

### 方法B: 使用终端命令
```bash
# 直接替换.env文件中的API密钥
sed -i '' 's/OPENAI_API_KEY=.*/OPENAI_API_KEY=sk-proj-your-actual-key-here/' .env

# 验证修改
grep OPENAI_API_KEY .env
```

### 方法C: 设置环境变量
```bash
# 临时设置 (当前终端会话有效)
export OPENAI_API_KEY='sk-proj-your-actual-key-here'

# 验证设置
echo $OPENAI_API_KEY

# 永久设置 (添加到 ~/.zshrc 或 ~/.bash_profile)
echo 'export OPENAI_API_KEY="sk-proj-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## 🧪 测试配置

### 快速测试
```bash
# 测试API连接
python3 -c "
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'sk-proj-your-key-here'))
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello, 测试连接'}],
    max_tokens=10
)
print('✅ API连接成功!')
print(f'回复: {response.choices[0].message.content}')
"
```

### 运行智能RAG测试
```bash
# 加载配置并运行
source .env && python3 smart_figureya_rag.py
```

## 🚀 体验AI功能

配置完成后，您将体验到:

### 智能搜索 vs 关键词搜索
- **基础版本**: "RNA-seq" → 匹配包含"RNA-seq"的文档
- **AI版本**: "如何分析RNA-seq数据" → 理解意图，推荐具体方法

### 专业回答 vs 模板回答
- **基础版本**: 固定的模块推荐
- **AI版本**: 基于您的具体需求生成个性化建议

### 高置信度分析
- **基础版本**: 置信度 0.65-0.75
- **AI版本**: 置信度 0.85-0.95

## 🔧 故障排除

### 常见错误及解决

1. **Invalid API key**
   ```
   解决: 检查API密钥是否正确，确保没有空格
   ```

2. **Insufficient credits**
   ```
   解决: 登录OpenAI平台充值
   ```

3. **Rate limit exceeded**
   ```
   解决: 等待几分钟后重试，或升级账户
   ```

4. **Connection error**
   ```
   解决: 检查网络连接，确保能访问OpenAI服务
   ```

### 调试命令
```bash
# 检查API密钥是否设置
echo $OPENAI_API_KEY

# 检查.env文件
cat .env | grep OPENAI_API_KEY

# 测试网络连接
curl -I https://api.openai.com

# 查看详细错误信息
python3 smart_figureya_rag.py 2>&1 | tee rag_debug.log
```

## 💰 费用说明

### OpenAI API定价 (GPT-3.5-turbo)
- **输入**: $0.001 per 1K tokens
- **输出**: $0.002 per 1K tokens
- **Embedding**: $0.0001 per 1K tokens

### 预估费用
- **轻度使用** (每天10-20个问题): $1-3/月
- **中度使用** (每天50-100个问题): $5-15/月
- **重度使用** (每天200+个问题): $20-50/月

## 📱 使用建议

1. **首次使用**: 先问几个简单问题测试功能
2. **专业咨询**: 利用AI的生物医学专业知识
3. **方法选择**: 询问适合您数据类型的分析方法
4. **参数优化**: 获取个性化的参数设置建议
5. **结果解读**: 让AI帮助解释复杂的分析结果

## 🎯 开始体验

配置完成后，运行以下命令开始体验:

```bash
# 方法1: 直接运行智能RAG
source .env && python3 smart_figureya_rag.py

# 方法2: 运行Web服务器
source .env && python3 figureya_rag_server_fixed.py

# 方法3: 使用交互式配置工具
python3 interactive_api_setup.py
```

---

**🎉 准备好体验真正的AI智能生物医学分析助手了吗？**