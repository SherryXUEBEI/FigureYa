#!/usr/bin/env python3
"""
智谱AI快速配置
一键配置GLM-4模型
"""

import os
import subprocess
import sys
from pathlib import Path

def quick_setup():
    """快速配置智谱AI"""
    print("🧠 智谱AI (GLM-4) 快速配置")
    print("=" * 40)

    # 1. 获取API密钥
    api_key = input("🔑 请输入智谱AI API密钥: ").strip()

    if not api_key:
        print("❌ API密钥不能为空")
        return False

    # 2. 安装SDK
    print("\n📦 安装智谱AI SDK...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "zhipuai"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ SDK安装成功")
    except:
        print("❌ SDK安装失败")
        return False

    # 3. 测试API
    print("\n🔍 测试API连接...")
    try:
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=api_key)
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": "测试"}],
            max_tokens=5
        )
        print("✅ API连接成功!")
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return False

    # 4. 保存配置
    print("\n💾 保存配置...")
    with open(".env", "a") as f:
        f.write(f"\n# 智谱AI配置\nZHIPUAI_API_KEY={api_key}\n")
    print("✅ 配置已保存")

    return True

if __name__ == "__main__":
    if quick_setup():
        print("\n🎉 配置完成!")
        print("🚀 运行命令:")
        print("export ZHIPUAI_API_KEY='your-key' && python3 zhipuai_rag_system.py")
    else:
        print("\n❌ 配置失败")
        print("💡 请检查API密钥和网络连接")