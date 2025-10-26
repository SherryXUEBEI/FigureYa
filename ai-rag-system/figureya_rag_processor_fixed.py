#!/usr/bin/env python3
"""
FigureYa RAG 智能生物医学分析助手
修复版本 - 处理SIGPIPE等信号问题
"""

import json
import os
import re
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from collections import defaultdict
import signal
import sys

# 修复SIGPIPE信号问题
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

class FigureYaRAGProcessor:
    """FigureYa RAG知识库处理器 - 修复版"""

    def __init__(self, figureya_path: str):
        self.figureya_path = Path(figureya_path)
        self.texts_path = self.figureya_path / "texts"
        self.chapters_json = self.figureya_path / "chapters.json"
        self.modules_path = self.figureya_path

        # 知识库存储
        self.knowledge_base = []
        self.module_index = {}
        self.technical_keywords = set()
        self.data_type_keywords = set()
        self.biology_keywords = set()

        # 缓存已处理的文件
        self._processed_files = set()

    def load_knowledge_base(self) -> List[Dict]:
        """加载并处理FigureYa知识库"""
        try:
            print("🚀 开始加载FigureYa知识库...")

            # 加载chapters索引
            chapters = []
            if self.chapters_json.exists():
                try:
                    with open(self.chapters_json, 'r', encoding='utf-8') as f:
                        chapters = json.load(f)
                    print(f"📚 加载了 {len(chapters)} 个模块索引")
                except (json.JSONDecodeError, IOError) as e:
                    print(f"⚠️ 无法加载章节索引: {e}")
                    chapters = []

            # 处理所有文本文件
            text_files = list(self.texts_path.glob("*.txt"))
            print(f"📄 发现 {len(text_files)} 个文本文件")

            # 限制处理数量以避免内存问题
            max_files = min(len(text_files), 200)  # 限制为200个文件
            text_files = text_files[:max_files]

            processed_count = 0
            for text_file in text_files:
                try:
                    if str(text_file) not in self._processed_files:
                        module_info = self._process_text_file(text_file, chapters)
                        if module_info:
                            self.knowledge_base.append(module_info)
                            self._processed_files.add(str(text_file))
                            processed_count += 1

                            # 每50个文件输出一次进度
                            if processed_count % 50 == 0:
                                print(f"📊 已处理 {processed_count}/{len(text_files)} 个文件")

                except Exception as e:
                    print(f"⚠️ 处理文件 {text_file} 时出错: {e}")
                    continue

            # 构建关键词索引
            self._build_keyword_index()

            print(f"✅ 成功加载 {len(self.knowledge_base)} 个模块的知识")
            return self.knowledge_base

        except Exception as e:
            print(f"❌ 加载知识库时发生错误: {e}")
            return []

    def _process_text_file(self, text_file: Path, chapters: List[Dict]) -> Dict:
        """处理单个文本文件"""
        try:
            # 提取模块ID
            module_id = text_file.stem

            # 查找对应的章节信息
            chapter_info = self._find_chapter_info(module_id, chapters)

            # 安全读取文本内容
            content = ""
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # 尝试其他编码
                try:
                    with open(text_file, 'r', encoding='gbk') as f:
                        content = f.read()
                except:
                    content = text_file.read_text(encoding='utf-8', errors='ignore')

            # 检查内容是否有效
            if len(content.strip()) < 50:
                return None

            # 提取模块信息
            module_info = {
                "id": module_id,
                "file_path": str(text_file),
                "content": content,
                "chapter_info": chapter_info,
                "word_count": len(content.split()),
                "lines_count": len(content.split('\n')),
            }

            # 智能分析内容
            module_info.update(self._analyze_content(content))

            return module_info

        except Exception as e:
            print(f"⚠️ 处理模块 {text_file} 时出错: {e}")
            return None

    def _find_chapter_info(self, module_id: str, chapters: List[Dict]) -> Dict:
        """查找模块对应的章节信息"""
        for chapter in chapters:
            if module_id in chapter.get("id", ""):
                return chapter
        return {}

    def _analyze_content(self, content: str) -> Dict:
        """智能分析内容，提取关键信息"""
        try:
            analysis = {
                "title": self._extract_title(content),
                "description": self._extract_description(content),
                "input_data_types": self._extract_input_data_types(content),
                "output_types": self._extract_output_types(content),
                "technical_methods": self._extract_technical_methods(content),
                "biology_areas": self._extract_biology_areas(content),
                "complexity_level": self._assess_complexity(content),
                "code_snippets": self._extract_code_snippets(content),
                "key_parameters": self._extract_key_parameters(content),
            }

            return analysis
        except Exception as e:
            print(f"⚠️ 分析内容时出错: {e}")
            return {
                "title": "未知标题",
                "description": "暂无描述",
                "input_data_types": [],
                "output_types": [],
                "technical_methods": [],
                "biology_areas": [],
                "complexity_level": "中级",
                "code_snippets": [],
                "key_parameters": []
            }

    def _extract_title(self, content: str) -> str:
        """提取标题"""
        try:
            lines = content.split('\n')
            for line in lines[:10]:  # 只检查前10行
                line = line.strip()
                if line and len(line) < 100:  # 合理的标题长度
                    # 匹配可能的标题模式
                    if re.match(r'^#{1,3}\s+', line) or \
                       re.match(r'^[A-Z][^.!?]*[.!?]?$', line) or \
                       "FigureYa" in line:
                        return line
            return "未知标题"
        except:
            return "未知标题"

    def _extract_description(self, content: str) -> str:
        """提取描述信息"""
        try:
            lines = content.split('\n')
            description_lines = []

            for i, line in enumerate(lines):
                line = line.strip()
                # 查找描述性关键词
                desc_keywords = ["需求描述", "应用场景", "功能", "分析", "可视化", "展示"]
                if any(keyword in line for keyword in desc_keywords):
                    # 收集接下来的几行作为描述
                    j = i + 1
                    while j < len(lines) and j < i + 5:
                        next_line = lines[j].strip()
                        if next_line and not next_line.startswith('#'):
                            description_lines.append(next_line)
                        j += 1
                    break

            return ' '.join(description_lines[:3]) if description_lines else "暂无描述"
        except:
            return "暂无描述"

    def _extract_input_data_types(self, content: str) -> List[str]:
        """提取输入数据类型"""
        try:
            data_types = []

            # 数据类型关键词映射
            data_type_patterns = {
                "RNA-seq": ["RNA-seq", "RNAseq", "转录组"],
                "DNA-seq": ["DNA-seq", "DNAseq", "基因组", "全基因组"],
                "ChIP-seq": ["ChIP-seq", "ChIPseq", "染色质免疫沉淀"],
                "单细胞": ["单细胞", "scRNA-seq", "single cell", "10x"],
                "蛋白质组": ["蛋白质组", "proteomics", "质谱"],
                "代谢组": ["代谢组", "metabolomics"],
                "临床数据": ["临床", "TCGA", "GEO", "病人", "样本"],
                "表达矩阵": ["表达矩阵", "expression matrix", "FPKM", "TPM"],
                "突变数据": ["突变", "mutation", "SNV", "CNV"],
                "生存数据": ["生存", "survival", "OS", "PFS"],
            }

            content_lower = content.lower()
            for data_type, keywords in data_type_patterns.items():
                if any(keyword in content_lower for keyword in keywords):
                    data_types.append(data_type)

            return list(set(data_types))
        except:
            return []

    def _extract_output_types(self, content: str) -> List[str]:
        """提取输出类型"""
        try:
            output_types = []

            output_patterns = {
                "热图": ["热图", "heatmap", "聚类图"],
                "火山图": ["火山图", "volcano", "差异表达"],
                "PCA图": ["PCA", "主成分", "降维"],
                "生存曲线": ["生存曲线", "survival", "Kaplan"],
                "箱线图": ["箱线图", "boxplot", "violin"],
                "散点图": ["散点图", "scatter", "correlation"],
                "网络图": ["网络", "network", "PPI", "互作"],
                "基因组浏览器": ["IGV", "genome browser", "基因组视图"],
                "统计表格": ["表格", "table", "统计"],
            }

            content_lower = content.lower()
            for output_type, keywords in output_patterns.items():
                if any(keyword in content_lower for keyword in keywords):
                    output_types.append(output_type)

            return list(set(output_types))
        except:
            return []

    def _extract_technical_methods(self, content: str) -> List[str]:
        """提取技术方法"""
        try:
            methods = []

            method_patterns = {
                "差异表达分析": ["差异表达", "differential expression", "DEG", "limma"],
                "聚类分析": ["聚类", "clustering", "hierarchical", "k-means"],
                "生存分析": ["生存分析", "cox", "logrank", "kaplan"],
                "通路分析": ["通路", "pathway", "GSEA", "富集"],
                "质量控制": ["质控", "QC", "质量控制", "quality"],
                "标准化": ["标准化", "normalization", "FPKM", "TPM"],
                "主成分分析": ["PCA", "主成分", "principal component"],
                "网络分析": ["网络分析", "network", "PPI", "STRING"],
                "motif分析": ["motif", "TF", "转录因子"],
            }

            content_lower = content.lower()
            for method, keywords in method_patterns.items():
                if any(keyword in content_lower for keyword in keywords):
                    methods.append(method)

            return list(set(methods))
        except:
            return []

    def _extract_biology_areas(self, content: str) -> List[str]:
        """提取生物学领域"""
        try:
            areas = []

            area_patterns = {
                "癌症研究": ["癌症", "cancer", "tumor", "TCGA"],
                "免疫学": ["免疫", "immune", "T细胞", "B细胞"],
                "神经科学": ["神经", "neuron", "brain"],
                "心血管": ["心脏", "心血管", "cardiovascular"],
                "代谢疾病": ["代谢", "糖尿病", "obesity"],
                "感染性疾病": ["感染", "病毒", "细菌"],
                "发育生物学": ["发育", "胚胎", "stem cell"],
                "药物研究": ["药物", "drug", "treatment"],
            }

            content_lower = content.lower()
            for area, keywords in area_patterns.items():
                if any(keyword in content_lower for keyword in keywords):
                    areas.append(area)

            return list(set(areas))
        except:
            return []

    def _assess_complexity(self, content: str) -> str:
        """评估复杂度"""
        try:
            complexity_indicators = {
                "高级": ["高级", "复杂", "多步骤", "综合"],
                "中级": ["中级", "常规", "标准"],
                "初级": ["简单", "基础", "入门", "快速"],
            }

            content_lower = content.lower()
            for level, keywords in complexity_indicators.items():
                if any(keyword in content_lower for keyword in keywords):
                    return level

            # 基于代码复杂度判断
            code_complexity = len([line for line in content.split('\n')
                                  if line.strip().startswith(('library(', 'require('))])

            if code_complexity > 10:
                return "高级"
            elif code_complexity > 5:
                return "中级"
            else:
                return "初级"
        except:
            return "中级"

    def _extract_code_snippets(self, content: str) -> List[str]:
        """提取代码片段"""
        try:
            code_snippets = []

            # 提取R代码块
            r_code_pattern = r'```{r[^}]*}(.*?)```'
            matches = re.findall(r_code_pattern, content, re.DOTALL)

            for match in matches:
                # 清理代码片段
                clean_code = re.sub(r'\n\s+', '\n', match.strip())
                if len(clean_code) > 20:  # 只保留有意义的代码片段
                    code_snippets.append(clean_code)

            return code_snippets[:3]  # 最多返回3个代码片段
        except:
            return []

    def _extract_key_parameters(self, content: str) -> List[str]:
        """提取关键参数"""
        try:
            parameters = []

            # 查找参数设置相关内容
            param_patterns = [
                r'(\w+)\s*=\s*["\']?\w+["\']?',  # 变量赋值
                r'(\w+)\s*=\s*\d+',             # 数值参数
                r'(\w+)\s*=\s*TRUE|FALSE',      # 逻辑参数
            ]

            content_lower = content.lower()
            for pattern in param_patterns:
                try:
                    matches = re.findall(pattern, content)
                    parameters.extend(matches)
                except:
                    continue

            # 提取常见的生物信息学参数
            common_params = ["pvalue", "adj.P.Val", "logFC", "FDR", "threshold", "min_size"]
            for param in common_params:
                if param in content_lower:
                    parameters.append(param)

            return list(set(parameters))[:10]  # 最多返回10个参数
        except:
            return []

    def _build_keyword_index(self):
        """构建关键词索引"""
        try:
            for module in self.knowledge_base:
                # 技术关键词
                self.technical_keywords.update(module.get("technical_methods", []))
                # 数据类型关键词
                self.data_type_keywords.update(module.get("input_data_types", []))
                # 生物学关键词
                self.biology_keywords.update(module.get("biology_areas", []))

            print(f"🔑 建立关键词索引:")
            print(f"   技术关键词: {len(self.technical_keywords)} 个")
            print(f"   数据类型关键词: {len(self.data_type_keywords)} 个")
            print(f"   生物学关键词: {len(self.biology_keywords)} 个")
        except Exception as e:
            print(f"⚠️ 构建关键词索引时出错: {e}")

    def search_modules(self, query: str, top_k: int = 5) -> List[Dict]:
        """基于关键词搜索相关模块"""
        try:
            if not self.knowledge_base:
                return []

            query_lower = query.lower()
            scored_modules = []

            for module in self.knowledge_base:
                score = self._calculate_relevance_score(query_lower, module)
                if score > 0:
                    module_copy = module.copy()
                    module_copy["relevance_score"] = score
                    scored_modules.append(module_copy)

            # 按相关性排序
            scored_modules.sort(key=lambda x: x["relevance_score"], reverse=True)

            return scored_modules[:top_k]
        except Exception as e:
            print(f"⚠️ 搜索模块时出错: {e}")
            return []

    def _calculate_relevance_score(self, query: str, module: Dict) -> float:
        """计算模块与查询的相关性得分"""
        try:
            score = 0.0
            content_lower = module.get("content", "").lower()

            # 完整匹配得分更高
            if query in content_lower:
                score += 10.0

            # 关键词匹配
            query_words = query.split()

            # 技术方法匹配
            for method in module.get("technical_methods", []):
                if any(word in method.lower() for word in query_words):
                    score += 3.0

            # 数据类型匹配
            for data_type in module.get("input_data_types", []):
                if any(word in data_type.lower() for word in query_words):
                    score += 2.5

            # 输出类型匹配
            for output_type in module.get("output_types", []):
                if any(word in output_type.lower() for word in query_words):
                    score += 2.0

            # 生物学领域匹配
            for area in module.get("biology_areas", []):
                if any(word in area.lower() for word in query_words):
                    score += 1.5

            # 标题匹配
            title = module.get("title", "").lower()
            if any(word in title for word in query_words):
                score += 4.0

            return score
        except:
            return 0.0

    def get_module_recommendations(self, data_type: str, analysis_goal: str) -> List[Dict]:
        """基于数据类型和分析目标推荐模块"""
        query = f"{data_type} {analysis_goal}"
        return self.search_modules(query, top_k=3)

    def export_knowledge_base(self, output_file: str = "figureya_knowledge_base.json"):
        """导出知识库为JSON文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
            print(f"✅ 知识库已导出到: {output_file}")
        except Exception as e:
            print(f"⚠️ 导出知识库时出错: {e}")

    def generate_summary_report(self) -> str:
        """生成知识库摘要报告"""
        try:
            total_modules = len(self.knowledge_base)

            # 统计各类模块数量
            data_type_counts = defaultdict(int)
            method_counts = defaultdict(int)
            complexity_counts = defaultdict(int)

            for module in self.knowledge_base:
                for data_type in module.get("input_data_types", []):
                    data_type_counts[data_type] += 1
                for method in module.get("technical_methods", []):
                    method_counts[method] += 1
                complexity = module.get("complexity_level", "未知")
                complexity_counts[complexity] += 1

            report = f"""
# FigureYa 知识库摘要报告

## 📊 基本统计
- **总模块数**: {total_modules}
- **技术方法种类**: {len(method_counts)}
- **数据类型种类**: {len(data_type_counts)}
- **复杂度分布**: {dict(complexity_counts)}

## 🔥 热门技术方法
"""

            # 按使用频率排序
            top_methods = sorted(method_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for method, count in top_methods:
                report += f"- **{method}**: {count} 个模块\n"

            report += "\n## 📈 主要数据类型\n"
            top_data_types = sorted(data_type_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for data_type, count in top_data_types:
                report += f"- **{data_type}**: {count} 个模块\n"

            return report
        except Exception as e:
            print(f"⚠️ 生成报告时出错: {e}")
            return "# 生成报告时出错"

    def cleanup(self):
        """清理资源"""
        self.knowledge_base.clear()
        self.technical_keywords.clear()
        self.data_type_keywords.clear()
        self.biology_keywords.clear()
        self._processed_files.clear()


def main():
    """主函数"""
    try:
        # 修复SIGPIPE
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        print("🧠 FigureYa RAG 智能生物医学分析助手")
        print("=" * 50)

        # 初始化处理器
        processor = FigureYaRAGProcessor("/Users/mypro/Downloads/FigureYa")

        # 加载知识库
        knowledge_base = processor.load_knowledge_base()

        if not knowledge_base:
            print("❌ 无法加载知识库，程序退出")
            return

        # 示例查询
        test_queries = [
            "差异表达分析 RNA-seq",
            "生存分析 临床数据",
            "单细胞 质量控制",
            "PCA 降维",
            "热图 聚类"
        ]

        print("\n🔍 测试查询结果:")
        for query in test_queries:
            try:
                results = processor.search_modules(query, top_k=3)
                print(f"\n查询: {query}")
                for i, result in enumerate(results, 1):
                    title = result.get("title", "未知标题")
                    score = result.get("relevance_score", 0)
                    print(f"  {i}. {title} (相关性: {score:.1f})")
            except Exception as e:
                print(f"  ⚠️ 查询 '{query}' 时出错: {e}")

        # 导出知识库
        try:
            processor.export_knowledge_base()
        except Exception as e:
            print(f"⚠️ 导出知识库时出错: {e}")

        # 生成摘要报告
        try:
            report = processor.generate_summary_report()
            with open("figureya_summary_report_fixed.md", "w", encoding="utf-8") as f:
                f.write(report)
            print("\n📄 摘要报告已生成: figureya_summary_report_fixed.md")
        except Exception as e:
            print(f"⚠️ 生成报告时出错: {e}")

        # 清理资源
        processor.cleanup()

    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
    finally:
        print("\n✅ 程序执行完毕")


if __name__ == "__main__":
    main()