#!/usr/bin/env python3
"""
FigureYa 智能RAG系统 - 完整演示版本
包含API配置和智能问答演示
"""

import os
import sys
from pathlib import Path

def load_env_file():
    """加载.env文件"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

def check_api_setup():
    """检查API设置状态"""
    print("🔍 检查API配置状态...")

    # 加载.env文件
    load_env_file()

    api_key = os.getenv("OPENAI_API_KEY", "")

    if api_key and api_key != "your-openai-api-key-here":
        print(f"✅ OpenAI API密钥已配置: {api_key[:10]}...")
        return True
    else:
        print("❌ OpenAI API密钥未配置")
        print("💡 将使用本地演示模式")
        return False

def main():
    """主函数"""
    print("🧠 FigureYa 智能RAG系统 - 完整演示")
    print("=" * 50)

    # 检查API配置
    has_api = check_api_setup()

    print("\n📋 运行选项:")
    print("1. 运行智能RAG演示 (无需API密钥)")
    print("2. 配置API密钥后运行完整版本")
    print("3. 查看API配置指南")

    choice = input("\n请选择 (1-3): ").strip()

    if choice == "1":
        print("\n🚀 运行智能RAG演示...")
        # 导入并运行演示系统
        try:
            from demo_smart_rag import SmartRAGDemo

            # 创建演示系统
            rag = SmartRAGDemo()

            print("\n🎯 智能问答演示:")
            print("-" * 40)

            # 运行几个测试查询
            test_queries = [
                "RNA-seq差异表达分析推荐什么模块？",
                "生存分析的参数如何设置？",
                "如何解释火山图的结果？"
            ]

            for i, query in enumerate(test_queries, 1):
                print(f"\n❓ 查询 {i}: {query}")
                result = rag.intelligent_search(query)

                print(f"🎯 意图识别: {result['intent']}")
                print(f"💬 智能回答:")
                print(result['response'][:200] + "..." if len(result['response']) > 200 else result['response'])
                print(f"📊 置信度: {result['confidence']:.2f}")
                print(f"🔗 相关模块: {', '.join(result['related_modules'])}")
                print("-" * 30)

        except Exception as e:
            print(f"❌ 演示运行失败: {e}")

    elif choice == "2":
        print("\n🔧 API配置指南:")
        print("=" * 30)
        print("1. 获取OpenAI API密钥: https://platform.openai.com/api-keys")
        print("2. 编辑配置文件: nano .env")
        print("3. 修改第6行: OPENAI_API_KEY=sk-your-actual-key-here")
        print("4. 保存后运行: python3 smart_figureya_rag.py")
        print("\n或使用配置工具:")
        print("./configure_api.sh")

    elif choice == "3":
        print("\n📖 详细配置指南:")
        print("=" * 30)
        print("\n🔑 方法1: 环境变量")
        print("export OPENAI_API_KEY='sk-your-key-here'")
        print("python3 smart_figureya_rag.py")

        print("\n🔑 方法2: .env文件")
        print("        # 1. 编辑.env文件")
        print("        nano .env")
        print("")
        print("        # 2. 修改这行:")
        print("        OPENAI_API_KEY=sk-your-actual-key-here")
        print("")
        print("        # 3. 保存并运行")
        print("        source .env")
        print("        python3 smart_figureya_rag.py")

        print("\n🔑 方法3: 命令行传递")
        print("OPENAI_API_KEY='sk-your-key-here' python3 smart_figureya_rag.py")

        print("\n📍 API密钥获取地址:")
        print("• OpenAI: https://platform.openai.com/api-keys")
        print("• Anthropic: https://console.anthropic.com/")
        print("• Google: https://makersuite.google.com/app/apikey")

    else:
        print("\n❌ 无效选择")

if __name__ == "__main__":
    main()