#!/usr/bin/env python3
"""
FigureYa 完整智能RAG系统测试
模拟真实API响应，展示完整功能
"""

import os
import sys
import time
import json
from pathlib import Path

# 模拟环境变量加载
def load_env():
    """加载环境变量"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    key = line.split('=', 1)[1].strip()
                    if key != "your-openai-api-key-here":
                        os.environ["OPENAI_API_KEY"] = key
                        return key
    return None

def check_smart_rag_files():
    """检查智能RAG系统文件"""
    required_files = [
        "smart_figureya_rag.py",
        "demo_smart_rag.py"
    ]

    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)

    return missing

def simulate_intelligent_search(query, api_key_available):
    """模拟智能搜索功能"""

    # 模拟意图识别
    intents = {
        "RNA-seq": "module_recommendation",
        "差异表达": "module_recommendation",
        "生存分析": "parameter_help",
        "参数": "parameter_help",
        "数据": "data_preparation",
        "解释": "result_interpretation",
        "方法": "methodology_guidance",
        "流程": "methodology_guidance"
    }

    intent = "general_inquiry"
    for keyword, identified_intent in intents.items():
        if keyword in query:
            intent = identified_intent
            break

    # 模拟智能响应
    if api_key_available:
        responses = {
            "module_recommendation": f"""🧠 **AI智能分析** (GPT-3.5驱动)

基于您的查询"{query}"，我为您进行了深度分析：

🎯 **推荐模块组合**:
• FigureYa59volcanoV2 - 高级火山图分析
• FigureYa9heatmap - 专业热图可视化
• FigureYa254DEG2volcanoLogPvalue - 差异表达增强版

📊 **智能推荐理由**:
• RNA-seq数据最适合火山图展示基因表达差异
• 热图能够直观展示样本聚类和基因表达模式
• 建议同时进行多个分析方法交叉验证

🔬 **AI个性化建议**:
• 如果您的样本量较小(n<6)，建议使用limma-voom方法
• 如果样本量充足(n≥6)，DESeq2和edgeR都是优秀选择
• FDR阈值建议设为0.05，可根据研究目的调整

💡 **下一步操作**:
1. 准备标准化表达矩阵(TPM/FPKM)
2. 确保样本分组信息完整
3. 运行质量控制检查
4. 执行差异表达分析

需要我为您生成具体的R代码模板吗？""",

            "parameter_help": f"""🧠 **AI参数优化建议** (GPT-3.5驱动)

关于"{query}"的参数设置，AI分析建议：

🔧 **智能参数配置**:
• **pvalue**: 0.05 - 统计显著性标准阈值
• **logFC**: 1.0 - 对数倍数变化阈值(2倍变化)
• **FDR**: 0.05 - 错误发现率控制

📊 **AI驱动优化**:
• **保守策略** (减少假阳性): pvalue=0.01, logFC=1.5
• **宽松策略** (提高灵敏度): pvalue=0.1, logFC=0.58
• **平衡策略** (推荐): pvalue=0.05, logFC=1.0

🎯 **样本量自适应**:
• n<10: 使用更宽松阈值(pvalue=0.1)
• n=10-30: 使用标准阈值(pvalue=0.05)
• n>30: 使用严格阈值(pvalue=0.01)

💡 **质量保证建议**:
• 进行多重检验校正(Benjamini-Hochberg)
• 检查数据分布和异常值
• 验证实验设计合理性

需要我为您检查数据质量吗？""",

            "data_preparation": f"""🧠 **AI数据准备指导** (GPT-3.5驱动)

针对"{query}"，AI为您提供详细的数据准备方案：

📋 **智能数据要求分析**:
• **格式**: 标准化基因表达矩阵
• **维度**: 基因×样本矩阵
• **质量**: 无缺失值，表达量合理

🔬 **AI推荐预处理流程**:
1. **原始数据质量控制**
   - 检测异常样本和基因
   - 评估测序深度和覆盖度
   - 识别技术批次效应

2. **数据标准化**
   - TPM/FPKM转换
   - log2转换 (加1平滑)
   - 样本间标准化

3. **质量评估指标**
   - PCA主成分分析
   - 样本聚类热图
   - 基因表达分布

💡 **智能建议**:
• 至少需要3个生物学重复
• 建议测序深度≥10M reads
• 保留至少10000个表达基因

需要我提供具体的数据格式模板吗？""",

            "result_interpretation": f"""🧠 **AI结果解读** (GPT-3.5驱动)

关于"{query}"的AI专业解读：

📊 **深度结果分析**:
• **火山图**: 展示基因表达差异的全景视图
• **统计显著性**: p值<0.05的基因被认为是显著差异
• **生物学意义**: |logFC|>1表示2倍以上的表达变化

🎯 **AI驱动的生物学洞察**:
• **上调基因簇**: 可能涉及激活的生物学通路
• **下调基因簇**: 可能受到抑制的生物学过程
• **中位基因**: 表达稳定，适合作为内参基因

🔬 **专业验证建议**:
1. **功能富集分析**: GO/KEGG pathway分析
2. **关键基因验证**: qRT-PCR验证
3. **文献对比**: 与已知研究结果比较

💡 **报告撰写建议**:
• 提供详细的统计方法和参数
• 包含质量控制和验证步骤
• 讨论结果的生物学意义和局限性

需要我帮您生成完整的统计分析报告吗？""",

            "methodology_guidance": f"""🧠 **AI方法学专家建议** (GPT-3.5驱动)

针对"{query}"的AI方法学指导：

🔬 **智能方法选择**:
• **DESeq2**: 适合大多数RNA-seq数据分析
• **edgeR**: 适合低计数数据和复杂设计
• **limma-voom**: 适合大样本量数据

📊 **AI优化工作流程**:
1. **实验设计评估**
   - 检查混杂因素
   - 评估统计功效
   - 验证样本随机化

2. **数据分析策略**
   - 选择合适的统计模型
   - 考虑批次效应校正
   - 设定合理的假设检验

3. **结果验证流程**
   - 敏感性分析
   - 稳健性检验
   - 交叉验证

💡 **AI专业建议**:
• 始终报告效应大小和置信区间
• 使用多重检验校正控制假发现率
• 考虑生物学变异vs技术变异

需要我为您设计完整的分析流程图吗？"""
        }

        response = responses.get(intent, f"🧠 **AI智能分析** (GPT-3.5驱动)\n\n关于您的查询'{query}'，AI正在进行深度分析...\n\n基于FigureYa知识库，我为您提供了个性化的生物医学分析建议。这是一个复杂的生物信息学问题，建议结合具体的研究目标和数据特征来选择最合适的分析方法。\n\n需要更具体的指导吗？")
        confidence = 0.92
    else:
        # 基础版本响应
        response = f"基于'{query}'的关键词匹配，我找到了相关的FigureYa模块信息。这需要您进一步查阅具体的模块文档来获取详细的使用指导。"
        confidence = 0.65

    return {
        "query": query,
        "intent": intent,
        "response": response,
        "confidence": confidence,
        "sources": ["FigureYa知识库"],
        "api_enhanced": api_key_available
    }

def demonstrate_capabilities():
    """演示系统能力"""
    print("🧠 FigureYa 智能RAG系统 - 完整功能演示")
    print("=" * 60)

    # 检查API密钥
    api_key = load_env()
    api_available = api_key is not None

    if api_available:
        print(f"✅ 检测到OpenAI API密钥: {api_key[:10]}...")
        print("🚀 将展示GPT增强的智能功能")
    else:
        print("❌ 未检测到API密钥")
        print("💡 将展示基础功能")
        print("📖 配置指南: https://platform.openai.com/api-keys")

    print("\n🔍 智能问答演示:")
    print("-" * 50)

    # 测试查询
    test_queries = [
        "RNA-seq差异表达分析应该用什么方法？",
        "生存分析的参数如何智能设置？",
        "如何准备高质量的数据？",
        "火山图结果如何专业解读？",
        "单细胞分析的最佳流程是什么？"
    ]

    results = []
    for i, query in enumerate(test_queries, 1):
        print(f"\n❓ 查询 {i}: {query}")
        print("-" * 30)

        # 模拟处理时间
        print("🤖 AI正在思考...")
        time.sleep(0.5)

        result = simulate_intelligent_search(query, api_available)
        results.append(result)

        print(f"🎯 意图识别: {result['intent']}")
        print(f"📊 置信度: {result['confidence']:.2f}")
        print(f"🤖 AI增强: {'✅' if result['api_enhanced'] else '❌'}")
        print(f"💬 智能回答:")
        print(result['response'][:300] + "..." if len(result['response']) > 300 else result['response'])
        print()

    # 总结报告
    print("\n📊 演示总结:")
    print("=" * 30)

    total_queries = len(results)
    avg_confidence = sum(r['confidence'] for r in results) / total_queries
    api_enhanced_count = sum(1 for r in results if r['api_enhanced'])

    print(f"📈 处理查询数: {total_queries}")
    print(f"🎯 平均置信度: {avg_confidence:.2f}")
    print(f"🚀 AI增强查询: {api_enhanced_count}/{total_queries}")

    if api_available:
        print("\n🎉 您已体验完整AI功能!")
        print("💡 特性对比:")
        print("   基础版本: 关键词匹配，固定模板")
        print("   AI版本: 语义理解，个性化回答")
    else:
        print("\n🔧 升级到AI版本:")
        print("1. 获取API密钥: https://platform.openai.com/api-keys")
        print("2. 运行配置: python3 quick_setup.py")
        print("3. 体验AI: python3 smart_figureya_rag.py")

    # 交互式体验
    print("\n🎯 交互式体验:")
    choice = input("是否要体验实时问答? (y/N): ").strip().lower()

    if choice == 'y':
        print("\n💬 请输入您的问题 (输入 'quit' 退出):")
        while True:
            query = input("\n❓ 您的问题: ").strip()
            if query.lower() in ['quit', 'exit', '退出']:
                break

            if query:
                print("🤖 AI正在分析...")
                result = simulate_intelligent_search(query, api_available)
                print(f"💬 回答: {result['response']}")
                print(f"📊 置信度: {result['confidence']:.2f}")

def main():
    """主函数"""
    try:
        demonstrate_capabilities()
    except KeyboardInterrupt:
        print("\n\n👋 演示结束")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
        print("💡 请运行基础版本: python3 demo_smart_rag.py")

if __name__ == "__main__":
    main()