#!/usr/bin/env python3
"""
FigureYa 一键配置和测试脚本
自动配置API密钥并展示智能功能
"""

import os
import subprocess
import sys
from pathlib import Path

def create_sample_env_with_demo_key():
    """创建带演示API密钥的.env文件"""
    demo_content = """# FigureYa 智能RAG系统 API配置
# 配置指南: https://platform.openai.com/api-keys

# OpenAI API (推荐)
# 获取地址: https://platform.openai.com/api-keys
# 格式: sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=demo-key-for-testing

# 可选配置
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
CHUNK_SIZE=500
TOP_K=5
"""

    with open(".env", 'w') as f:
        f.write(demo_content)

    print("📝 已创建演示配置文件")

def install_dependencies():
    """安装必要依赖"""
    packages = ["openai", "numpy", "requests"]

    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"📥 正在安装 {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def demo_ai_responses():
    """演示AI增强的响应"""
    demo_responses = [
        {
            "query": "RNA-seq差异表达分析推荐什么模块？",
            "intent": "module_recommendation",
            "response": """🧠 **AI智能分析** (GPT-3.5驱动)

基于您的查询，我为您进行了深度分析：

🎯 **推荐模块组合**:
• FigureYa59volcanoV2 - 高级火山图分析
• FigureYa9heatmap - 专业热图可视化
• FigureYa254DEG2volcanoLogPvalue - 差异表达增强版

📊 **智能推荐理由**:
• RNA-seq数据最适合火山图展示基因表达差异
• 热图能够直观展示样本聚类和基因表达模式
• 建议同时进行多个分析方法交叉验证

🔬 **AI个性化建议**:
• 如果样本量较小(n<6)，建议使用limma-voom方法
• 如果样本量充足(n≥6)，DESeq2和edgeR都是优秀选择
• FDR阈值建议设为0.05，可根据研究目的调整

💡 **下一步操作**:
1. 准备标准化表达矩阵(TPM/FPKM)
2. 确保样本分组信息完整
3. 运行质量控制检查
4. 执行差异表达分析

需要我为您生成具体的R代码模板吗？""",
            "confidence": 0.95,
            "api_enhanced": True
        },
        {
            "query": "生存分析的参数如何设置？",
            "intent": "parameter_help",
            "response": """🧠 **AI参数优化建议** (GPT-3.5驱动)

关于生存分析的参数设置，AI分析建议：

🔧 **智能参数配置**:
• **pvalue**: 0.05 - 统计显著性标准阈值
• **conf_int**: 0.95 - 置信区间范围
• **method**: Kaplan-Meier - 生存曲线估计方法

📊 **AI驱动优化**:
• **保守策略** (减少假阳性): pvalue=0.01
• **宽松策略** (提高灵敏度): pvalue=0.1
• **平衡策略** (推荐): pvalue=0.05

🎯 **样本量自适应**:
• n<50: 使用更宽松阈值(pvalue=0.1)
• n=50-200: 使用标准阈值(pvalue=0.05)
• n>200: 使用严格阈值(pvalue=0.01)

💡 **质量保证建议**:
• 检查比例风险假设
• 进行多重检验校正
• 验证模型拟合优度

需要我帮您检查数据质量吗？""",
            "confidence": 0.93,
            "api_enhanced": True
        },
        {
            "query": "如何解释火山图的结果？",
            "intent": "result_interpretation",
            "response": """🧠 **AI结果解读** (GPT-3.5驱动)

关于火山图结果的AI专业解读：

📊 **深度结果分析**:
• **火山图**: 展示基因表达差异的全景视图
• **X轴**: logFC (对数倍数变化)
  - 正值 → 上调基因
  - 负值 → 下调基因
  - |logFC| > 1 = 2倍变化
• **Y轴**: -log10(P.Value)
  - 值越大越显著
  - 阈值线: -log10(0.05) ≈ 1.3

🎯 **AI驱动的生物学洞察**:
• **右上角**: 显著上调基因 (可能激活的通路)
• **左上角**: 显著下调基因 (可能抑制的通路)
• **中间区域**: 不显著基因 (表达稳定)

🔬 **专业验证建议**:
1. **功能富集分析**: GO/KEGG pathway分析
2. **关键基因验证**: qRT-PCR验证
3. **文献对比**: 与已知研究比较

💡 **报告撰写建议**:
• 提供详细的统计方法和参数
• 包含质量控制和验证步骤
• 讨论结果的生物学意义和局限性

需要我帮您生成完整的统计分析报告吗？""",
            "confidence": 0.94,
            "api_enhanced": True
        }
    ]

    return demo_responses

def main():
    """主流程"""
    print("🧠 FigureYa 智能RAG系统 - 一键配置演示")
    print("=" * 60)

    # 1. 创建配置文件
    print("\n📋 步骤1: 创建配置文件")
    create_sample_env_with_demo_key()

    # 2. 安装依赖
    print("\n📋 步骤2: 检查依赖包")
    install_dependencies()

    # 3. 演示AI功能
    print("\n📋 步骤3: 演示AI智能功能")
    print("🚀 模拟GPT-3.5驱动的智能分析")
    print("-" * 50)

    demo_responses = demo_ai_responses()

    for i, demo in enumerate(demo_responses, 1):
        print(f"\n❓ 查询 {i}: {demo['query']}")
        print(f"🎯 意图识别: {demo['intent']}")
        print(f"📊 置信度: {demo['confidence']:.2f}")
        print(f"🤖 AI增强: {'✅' if demo['api_enhanced'] else '❌'}")
        print(f"💬 智能回答:")
        print(demo['response'])
        print("-" * 50)

    # 4. 配置指南
    print("\n📋 步骤4: 真实API配置指南")
    print("=" * 30)
    print("🔑 获取真实API密钥:")
    print("   1. 访问: https://platform.openai.com/api-keys")
    print("   2. 注册/登录OpenAI账户")
    print("   3. 创建API密钥 (sk-proj-...)")
    print("   4. 充值账户 (建议$5-10)")
    print("")
    print("⚙️ 配置方法:")
    print("   方法1: 编辑 .env 文件")
    print("   方法2: export OPENAI_API_KEY='your-key'")
    print("   方法3: python3 quick_setup.py")
    print("")
    print("🚀 启动真实AI系统:")
    print("   source .env && python3 smart_figureya_rag.py")

    print("\n🎉 演示完成!")
    print("💡 对比:")
    print("   基础版本: 关键词匹配，模板化回答")
    print("   AI版本: 语义理解，个性化专业建议")
    print("")
    print("📖 更多信息:")
    print("   • 配置指南: open api_setup_guide.html")
    print("   • 快速配置: python3 quick_setup.py")
    print("   • 基础演示: python3 demo_smart_rag.py")

if __name__ == "__main__":
    main()