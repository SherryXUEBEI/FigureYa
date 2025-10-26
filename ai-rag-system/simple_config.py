#!/usr/bin/env python3
"""
简单API配置脚本
直接替换.env文件中的API密钥
"""

import os
import subprocess
from pathlib import Path

def update_api_key():
    """更新API密钥"""
    print("🔑 FigureYa API密钥配置")
    print("=" * 30)

    # 1. 获取API密钥
    print("📍 获取OpenAI API密钥:")
    print("   1. 访问: https://platform.openai.com/api-keys")
    print("   2. 创建并复制API密钥")
    print("   3. 格式: sk-proj-xxxxxxxxxxx")

    api_key = input("\n请输入您的API密钥: ").strip()

    if not api_key:
        print("❌ API密钥不能为空")
        return False

    if not api_key.startswith("sk-"):
        print("⚠️ API密钥格式可能不正确")
        confirm = input("继续吗? (y/N): ").strip().lower()
        if confirm != 'y':
            return False

    # 2. 更新.env文件
    env_path = Path(".env")
    if env_path.exists():
        # 读取现有内容
        with open(env_path, 'r') as f:
            content = f.read()

        # 替换API密钥
        content = content.replace("OPENAI_API_KEY=demo-key-for-testing",
                                f"OPENAI_API_KEY={api_key}")

        # 写回文件
        with open(env_path, 'w') as f:
            f.write(content)

        print(f"✅ API密钥已更新")
        print(f"🔒 密钥: {api_key[:10]}...")

        # 3. 测试连接
        print("\n🔍 测试API连接...")
        try:
            import openai

            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "测试连接"}],
                max_tokens=5
            )
            print("✅ API连接成功!")
            return True

        except ImportError:
            print("⚠️ 需要安装openai包")
            subprocess.run([sys.executable, "-m", "pip", "install", "openai"])
            print("请重新运行此脚本")
            return False

        except Exception as e:
            print(f"❌ API连接失败: {e}")
            return False

    else:
        print("❌ 找不到.env文件")
        return False

if __name__ == "__main__":
    if update_api_key():
        print("\n🎉 配置完成!")
        print("🚀 运行智能RAG: source .env && python3 smart_figureya_rag.py")
    else:
        print("❌ 配置失败")
        print("💡 手动编辑 .env 文件或查看配置指南")