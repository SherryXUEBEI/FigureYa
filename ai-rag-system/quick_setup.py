#!/usr/bin/env python3
"""
FigureYa 快速API配置工具
一键配置并测试OpenAI API
"""

import os
import sys
import subprocess
from pathlib import Path

def get_user_input():
    """获取用户输入"""
    try:
        # 在支持的终端中获取输入
        if sys.stdin.isatty():
            import getpass
            api_key = getpass.getpass("🔑 请输入您的OpenAI API密钥 (sk-...): ")
            return api_key.strip()
        else:
            # 备用方法
            print("🔑 请输入您的OpenAI API密钥:")
            print("   获取地址: https://platform.openai.com/api-keys")
            print("   密钥格式: sk-...")
            return input("API密钥: ").strip()
    except:
        return input("🔑 请输入您的OpenAI API密钥: ").strip()

def validate_api_key(api_key):
    """验证API密钥格式"""
    if not api_key:
        return False
    if not api_key.startswith("sk-"):
        print("⚠️ OpenAI API密钥通常以 'sk-' 开头")
        choice = input("确定要继续吗? (y/N): ").strip().lower()
        return choice == 'y'
    if len(api_key) < 20:
        print("⚠️ API密钥长度似乎太短")
        choice = input("确定要继续吗? (y/N): ").strip().lower()
        return choice == 'y'
    return True

def save_to_env_file(api_key):
    """保存API密钥到.env文件"""
    env_path = Path(".env")

    # 创建或更新.env文件
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
    return True

def install_openai_package():
    """安装OpenAI包"""
    print("📦 检查并安装OpenAI包...")
    try:
        import openai
        print("✅ OpenAI包已安装")
        return True
    except ImportError:
        print("📥 正在安装OpenAI包...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
            print("✅ OpenAI包安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ OpenAI包安装失败")
            print("💡 请手动运行: pip install openai")
            return False

def test_openai_connection(api_key):
    """测试OpenAI API连接"""
    print("🔍 测试API连接...")

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        # 测试简单请求
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "请回复'连接成功'"}],
            max_tokens=10
        )

        result = response.choices[0].message.content.strip()
        print(f"✅ API连接成功!")
        print(f"💬 GPT回复: {result}")
        return True

    except Exception as e:
        print(f"❌ API连接失败: {e}")
        print("\n💡 可能的原因:")
        print("   • API密钥无效或已过期")
        print("   • 账户余额不足")
        print("   • 网络连接问题")
        print("   • OpenAI服务暂时不可用")
        return False

def run_smart_rag_demo():
    """运行智能RAG演示"""
    print("\n🚀 启动智能RAG系统...")
    print("   " + "="*40)

    # 加载环境变量
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    key = line.split('=', 1)[1].strip()
                    os.environ["OPENAI_API_KEY"] = key
                    break

    try:
        # 导入并运行智能系统
        subprocess.run([sys.executable, "smart_figureya_rag.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ 智能RAG系统运行失败")
        print("💡 请检查配置或运行演示版本: python3 demo_smart_rag.py")

def main():
    """主配置流程"""
    print("🧠 FigureYa 智能RAG系统 - 快速配置")
    print("=" * 50)

    # 1. 获取API密钥
    print("\n📋 步骤1: 配置API密钥")
    api_key = get_user_input()

    if not validate_api_key(api_key):
        print("❌ API密钥验证失败")
        return

    # 2. 保存到.env文件
    if not save_to_env_file(api_key):
        print("❌ 保存API密钥失败")
        return

    # 3. 安装依赖
    print("\n📋 步骤2: 检查依赖")
    if not install_openai_package():
        print("❌ 依赖安装失败，无法继续")
        return

    # 4. 测试API连接
    print("\n📋 步骤3: 测试API连接")
    if not test_openai_connection(api_key):
        print("❌ API测试失败，请检查密钥或网络")
        return

    # 5. 运行智能系统
    print("\n📋 步骤4: 启动智能RAG系统")

    choice = input("是否现在运行智能RAG系统? (Y/n): ").strip().lower()
    if choice != 'n':
        run_smart_rag_demo()

    print("\n🎉 配置完成!")
    print("💡 以后可以直接运行: python3 smart_figureya_rag.py")

if __name__ == "__main__":
    main()