#!/usr/bin/env python3
"""
FigureYa RAG 智能问答系统
基于FigureYa知识库的生物医学分析助手
"""

import json
import re
from typing import List, Dict, Tuple
from figureya_rag_processor import FigureYaRAGProcessor

class FigureYaRAGChat:
    """FigureYa RAG智能问答系统"""

    def __init__(self, figureya_path: str):
        self.processor = FigureYaRAGProcessor(figureya_path)
        self.knowledge_base = self.processor.load_knowledge_base()
        self.conversation_history = []

        # 预定义的意图分类
        self.intent_patterns = {
            "module_recommendation": [
                "推荐", "建议", "哪个", "什么", "如何", "用哪个", "应该用"
            ],
            "parameter_help": [
                "参数", "设置", "配置", "如何设置", "什么参数"
            ],
            "data_preparation": [
                "数据格式", "输入", "准备", "需要什么", "格式"
            ],
            "result_interpretation": [
                "解释", "意义", "怎么看", "说明", "理解"
            ],
            "troubleshooting": [
                "错误", "失败", "不work", "问题", "bug"
            ]
        }

    def chat(self, user_query: str) -> Dict:
        """处理用户查询"""
        # 记录对话历史
        self.conversation_history.append({"role": "user", "content": user_query})

        # 分析意图
        intent = self._analyze_intent(user_query)

        # 检索相关知识
        relevant_modules = self.processor.search_modules(user_query, top_k=5)

        # 生成回答
        response = self._generate_response(user_query, intent, relevant_modules)

        # 记录回答
        self.conversation_history.append({"role": "assistant", "content": response["text"]})

        return response

    def _analyze_intent(self, query: str) -> str:
        """分析用户意图"""
        query_lower = query.lower()

        # 计算每个意图的匹配得分
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            intent_scores[intent] = score

        # 返回得分最高的意图
        if max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        else:
            return "general_inquiry"

    def _generate_response(self, query: str, intent: str, modules: List[Dict]) -> Dict:
        """生成智能回答"""
        if not modules:
            return {
                "text": "抱歉，我没有找到与您查询相关的模块。请尝试使用更具体的关键词，比如'RNA-seq差异表达分析'或'生存曲线'。",
                "modules": [],
                "intent": intent
            }

        # 根据意图生成不同类型的回答
        if intent == "module_recommendation":
            return self._generate_module_recommendation(query, modules)
        elif intent == "parameter_help":
            return self._generate_parameter_help(query, modules)
        elif intent == "data_preparation":
            return self._generate_data_preparation_help(query, modules)
        elif intent == "result_interpretation":
            return self._generate_result_interpretation(query, modules)
        else:
            return self._generate_general_response(query, modules)

    def _generate_module_recommendation(self, query: str, modules: List[Dict]) -> Dict:
        """生成模块推荐回答"""
        if not modules:
            return {"text": "未找到相关模块", "modules": [], "intent": "module_recommendation"}

        top_module = modules[0]
        title = top_module.get("title", "未知模块")
        description = top_module.get("description", "")
        input_types = top_module.get("input_data_types", [])
        output_types = top_module.get("output_types", [])
        complexity = top_module.get("complexity_level", "中级")

        response = f"""根据您的查询，我为您推荐以下模块：

## 🎯 主要推荐：{title}

**复杂度**: {complexity}
**输入数据类型**: {', '.join(input_types) if input_types else '通用数据'}
**输出结果**: {', '.join(output_types) if output_types else '可视化图表'}

**功能描述**: {description[:200]}...

---

"""

        # 如果有多个相关模块，提供更多选择
        if len(modules) > 1:
            response += "## 🔄 其他相关模块\n\n"
            for i, module in enumerate(modules[1:3], 2):
                module_title = module.get("title", "未知模块")
                module_input = module.get("input_data_types", [])
                response += f"{i}. **{module_title}**\n"
                response += f"   - 数据类型: {', '.join(module_input) if module_input else '通用'}\n\n"

        response += """
## 💡 使用建议

1. **新手用户**: 建议从初级复杂度的模块开始
2. **数据准备**: 确保您的数据格式符合模块要求
3. **参数调整**: 根据数据特征调整关键参数
4. **结果验证**: 使用多个模块交叉验证结果

需要更详细的使用指导吗？
"""

        return {
            "text": response,
            "modules": modules[:3],
            "intent": "module_recommendation"
        }

    def _generate_parameter_help(self, query: str, modules: List[Dict]) -> Dict:
        """生成参数帮助回答"""
        # 收集所有相关参数
        all_parameters = set()
        for module in modules:
            all_parameters.update(module.get("key_parameters", []))

        if not all_parameters:
            return {
                "text": "我没有找到相关模块的参数信息。请查看具体的模块文档获取详细参数说明。",
                "modules": modules,
                "intent": "parameter_help"
            }

        response = f"""## 📋 相关参数说明

基于相关模块，以下是主要参数的设置建议：

"""

        # 常见参数的说明
        parameter_help = {
            "pvalue": "显著性阈值，通常设置为0.05或更严格",
            "adj.P.Val": "校正后的p值，建议使用0.05作为阈值",
            "logFC": "对数倍数变化，绝对值越大表示差异越显著",
            "FDR": "错误发现率，控制假阳性",
            "threshold": "筛选阈值，根据具体分析目标调整",
            "min_size": "最小样本数或基因集大小",
        }

        for param in sorted(all_parameters)[:10]:
            help_text = parameter_help.get(param, "具体参数请参考模块文档")
            response += f"• **{param}**: {help_text}\n"

        response += f"""

## 🎯 推荐模块

最相关的模块是：**{modules[0].get('title', '未知模块')}**

建议您查看该模块的完整文档了解所有参数的详细说明和推荐值。
"""

        return {
            "text": response,
            "modules": modules[:2],
            "intent": "parameter_help"
        }

    def _generate_data_preparation_help(self, query: str, modules: List[Dict]) -> Dict:
        """生成数据准备帮助回答"""
        # 收集输入数据类型信息
        input_types = set()
        for module in modules:
            input_types.update(module.get("input_data_types", []))

        response = f"""## 📊 数据准备指南

根据您的查询和推荐模块，您需要准备以下类型的数据：

### 🎯 主要数据类型
{', '.join(input_types) if input_types else '标准表格数据'}

### 📁 常见数据格式要求

**1. 表达数据 (Expression Data)**
```
Gene    Sample1    Sample2    Sample3
TP53    5.2        3.8        4.1
BRCA1   2.1        6.3        4.5
...
```

**2. 临床数据 (Clinical Data)**
```
Sample    Age    Sex    Survival    Status
Patient1  65     M      365         1
Patient2  58     F      720         0
...
```

**3. 差异表达结果 (Differential Expression)**
```
Gene    logFC    P.Value    adj.P.Val
GeneA    2.3     0.001      0.01
GeneB   -1.8     0.003      0.02
...
```

### ⚠️ 注意事项
- 确保基因/样本命名一致性
- 检查数据完整性和格式正确性
- 根据分析需求进行适当的数据预处理

## 🎯 推荐处理流程
"""

        # 推荐处理模块序列
        preprocessing_modules = []
        for module in modules[:3]:
            if "标准化" in module.get("technical_methods", []):
                preprocessing_modules.append(module)

        if preprocessing_modules:
            response += "\n建议的数据预处理模块：\n"
            for module in preprocessing_modules:
                title = module.get("title", "未知模块")
                response += f"• **{title}**\n"

        return {
            "text": response,
            "modules": modules[:3],
            "intent": "data_preparation"
        }

    def _generate_result_interpretation(self, query: str, modules: List[Dict]) -> Dict:
        """生成结果解释帮助"""
        # 分析模块的输出类型
        output_types = set()
        for module in modules:
            output_types.update(module.get("output_types", []))

        response = f"""## 📈 结果解读指南

基于您的查询，以下是主要可视化结果的生物学解读：

### 🎯 主要图表类型
{', '.join(output_types) if output_types else '统计图表'}

### 📊 常见图表解读

**火山图 (Volcano Plot)**
- X轴: logFC (对数倍数变化)，负值表示下调，正值表示上调
- Y轴: -log10(P.Value)，值越大越显著
- 右上角: 显著上调基因
- 左上角: 显著下调基因
- 中间区域: 差异不显著基因

**热图 (Heatmap)**
- 行: 基因/样本
- 列: 样本/基因
- 颜色: 表达量高低 (红色=高表达，蓝色=低表达)
- 聚类树: 基于表达模式的相似性聚类

**生存曲线 (Survival Curve)**
- X轴: 时间 (天/月/年)
- Y轴: 生存率
- 不同颜色: 不同组别
- 阴影区域: 95%置信区间

### 🔬 生物学意义

**差异表达分析结果**:
- 关注|logFC| > 1 且 adj.P.Val < 0.05 的基因
- 生物学功能富集分析 (GO/KEGG)
- 与疾病相关的已知基因验证

**生存分析结果**:
- HR (风险比) > 1: 高风险因素
- HR (风险比) < 1: 保护性因素
- P值 < 0.05: 统计学显著

## 💡 专业建议
建议结合生物学背景知识和文献验证分析结果的合理性。
"""

        return {
            "text": response,
            "modules": modules[:2],
            "intent": "result_interpretation"
        }

    def _generate_general_response(self, query: str, modules: List[Dict]) -> Dict:
        """生成通用回答"""
        if not modules:
            return {
                "text": "抱歉，我没有找到与您查询相关的模块。请尝试使用更具体的关键词，比如技术方法名称、数据类型或分析目标。",
                "modules": [],
                "intent": "general_inquiry"
            }

        top_module = modules[0]
        title = top_module.get("title", "未知模块")
        description = top_module.get("description", "")
        methods = top_module.get("technical_methods", [])
        data_types = top_module.get("input_data_types", [])
        outputs = top_module.get("output_types", [])

        response = f"""## 🎯 相关模块：{title}

**技术方法**: {', '.join(methods) if methods else '综合分析'}
**适用数据**: {', '.join(data_types) if data_types else '多种数据类型'}
**输出结果**: {', '.join(outputs) if outputs else '可视化图表'}

**功能描述**: {description[:300] if description else '这是一个生物医学数据分析模块，提供专业的数据处理和可视化功能'}...

---

## 📚 更多相关信息

"""

        # 提供更多相关模块信息
        if len(modules) > 1:
            response += "**其他相关模块**:\n"
            for i, module in enumerate(modules[1:3], 2):
                module_title = module.get("title", "未知模块")
                module_methods = module.get("technical_methods", [])
                response += f"{i}. **{module_title}** - {', '.join(module_methods[:2]) if module_methods else '数据分析'}\n"

        response += """

## 💡 下一步建议
- 如果需要模块推荐，请询问"我应该用哪个模块来..."
- 如果需要参数帮助，请询问"如何设置参数..."
- 如果需要数据格式说明，请询问"需要什么格式的数据..."

还有什么具体问题需要了解吗？
"""

        return {
            "text": response,
            "modules": modules[:3],
            "intent": "general_inquiry"
        }

    def get_conversation_summary(self) -> str:
        """获取对话摘要"""
        if not self.conversation_history:
            return "还没有对话记录"

        user_queries = [msg["content"] for msg in self.conversation_history if msg["role"] == "user"]
        return f"""
## 📝 对话摘要

**对话轮次**: {len(user_queries)}
**用户查询**:
{chr(10).join(f"{i+1}. {query}" for i, query in enumerate(user_queries[-5:]))}

最后5次用户查询如上所示。
"""


def main():
    """主函数 - 启动RAG聊天系统"""
    print("🤖 FigureYa RAG 智能生物医学分析助手")
    print("=" * 50)
    print("输入 'quit' 退出对话")
    print("输入 'help' 查看使用指南")
    print("=" * 50)

    # 初始化RAG系统
    chat_system = FigureYaRAGChat("/Users/mypro/Downloads/FigureYa")

    # 示例对话
    example_queries = [
        "我想做RNA-seq差异表达分析，推荐什么模块？",
        "生存分析需要什么数据格式？",
        "如何解释火山图的结果？",
        "单细胞数据质量控制用什么工具？"
    ]

    print("\n💡 示例查询:")
    for i, query in enumerate(example_queries, 1):
        print(f"{i}. {query}")

    print("\n" + "=" * 50)

    # 交互式对话
    while True:
        try:
            user_input = input("\n👤 您: ").strip()

            if user_input.lower() == 'quit':
                print("\n👋 感谢使用FigureYa RAG助手！")
                break
            elif user_input.lower() == 'help':
                print("""
🆘 使用指南:
1. 描述您的数据类型和分析目标
2. 询问具体的参数设置
3. 请求结果解读帮助
4. 查询数据处理方法

示例:
- "RNA-seq数据分析推荐"
- "生存曲线参数设置"
- "如何理解热图结果"
                """)
                continue
            elif not user_input:
                continue

            # 处理查询
            print("\n🤖 助手正在思考...")
            response = chat_system.chat(user_input)

            print(f"\n🤖 助手:\n{response['text']}")
            print(f"\n📊 相关模块数: {len(response['modules'])}")
            print(f"🎯 意图识别: {response['intent']}")

        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 抱歉，出现错误: {e}")
            print("请重新输入您的问题。")


if __name__ == "__main__":
    main()