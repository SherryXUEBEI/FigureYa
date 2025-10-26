#!/usr/bin/env python3
"""
FigureYa API密钥配置工具
帮助用户设置和测试API密钥
"""

import os
import sys
from pathlib import Path

def setup_env_file():
    """设置.env文件"""
    env_path = Path(".env")
    example_path = Path(".env.example")

    if env_path.exists():
        print("✅ .env文件已存在")
        print(f"📍 位置: {env_path.absolute()}")
        return True

    if example_path.exists():
        # 复制示例文件
        import shutil
        shutil.copy(example_path, env_path)
        print(f"📝 已创建 .env 文件，请编辑: {env_path.absolute()}")
        print("\n🔧 请按以下步骤配置:")
        print("1. 打开 .env 文件")
        print("2. 替换 'your-xxx-api-key-here' 为您的真实API密钥")
        print("3. 保存文件")
        return True
    else:
        print("❌ 找不到 .env.example 文件")
        return False

def get_openai_key():
    """获取OpenAI API密钥"""
    # 优先从环境变量获取
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    # 尝试从.env文件读取
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    return line.split("=", 1)[1].strip()

    return None

def test_openai_api():
    """测试OpenAI API连接"""
    try:
        from openai import OpenAI

        api_key = get_openai_key()
        if not api_key:
            print("❌ 未找到OpenAI API密钥")
            print("💡 请设置环境变量或编辑.env文件")
            return False

        print("🔍 测试OpenAI API连接...")
        client = OpenAI(api_key=api_key)

        # 测试简单对话
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=10
        )

        print("✅ OpenAI API连接成功!")
        print(f"💬 回复: {response.choices[0].message.content.strip()}")
        return True

    except ImportError:
        print("❌ 未安装openai包，请运行: pip install openai")
        return False
    except Exception as e:
        print(f"❌ OpenAI API测试失败: {e}")
        return False

def get_user_api_key():
    """交互式获取用户API密钥"""
    print("\n🔑 请输入您的API密钥:")
    print("📍 获取OpenAI API密钥: https://platform.openai.com/api-keys")

    api_key = input("请输入您的OpenAI API密钥 (sk-...): ").strip()

    if not api_key.startswith("sk-"):
        print("⚠️ OpenAI API密钥通常以 'sk-' 开头")
        confirm = input("确定要继续吗? (y/N): ").strip().lower()
        if confirm != 'y':
            return None

    return api_key

def save_api_key_to_env(api_key):
    """保存API密钥到.env文件"""
    env_path = Path(".env")

    # 读取现有内容
    lines = []
    if env_path.exists():
        with open(env_path, 'r') as f:
            lines = f.readlines()

    # 更新或添加API密钥
    updated = False
    for i, line in enumerate(lines):
        if line.startswith("OPENAI_API_KEY="):
            lines[i] = f"OPENAI_API_KEY={api_key}\n"
            updated = True
            break

    if not updated:
        lines.append(f"OPENAI_API_KEY={api_key}\n")

    # 写回文件
    with open(env_path, 'w') as f:
        f.writelines(lines)

    print(f"✅ API密钥已保存到: {env_path.absolute()}")

def main():
    """主函数"""
    print("🔧 FigureYa API密钥配置工具")
    print("=" * 40)

    # 1. 设置.env文件
    if not setup_env_file():
        print("❌ 无法创建配置文件")
        return

    # 2. 检查现有API密钥
    current_key = get_openai_key()
    if current_key:
        print(f"✅ 找到现有API密钥: {current_key[:10]}...")

        # 询问是否测试
        test_choice = input("\n是否测试API连接? (Y/n): ").strip().lower()
        if test_choice != 'n':
            test_openai_api()
    else:
        print("❌ 未找到API密钥")

        # 询问是否输入
        input_choice = input("\n是否现在输入API密钥? (Y/n): ").strip().lower()
        if input_choice != 'n':
            api_key = get_user_api_key()
            if api_key:
                save_api_key_to_env(api_key)
                test_openai_api()

    print("\n📚 使用说明:")
    print("1. 永久设置: 在 ~/.bashrc 或 ~/.zshrc 中添加:")
    print(f"   export OPENAI_API_KEY=$(cat {Path.cwd()}/.env | grep OPENAI_API_KEY | cut -d'=' -f2)")
    print("\n2. 临时设置: 在终端中运行:")
    print("   export OPENAI_API_KEY=your-key-here")
    print("\n3. 运行智能RAG:")
    print("   python3 smart_figureya_rag.py")

if __name__ == "__main__":
    main()