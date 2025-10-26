#!/usr/bin/env python3
"""
FigureYa 交互式API密钥配置工具
引导用户完成真实API密钥配置
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def clear_screen():
    """清屏"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    """打印标题"""
    clear_screen()
    print("🧠 FigureYa 智能RAG系统 - 真实API密钥配置")
    print("=" * 60)
    print("🚀 即将体验真正的GPT-3.5智能功能！")
    print("=" * 60)

def step1_get_api_key():
    """步骤1: 获取API密钥"""
    print("\n📋 步骤 1/4: 获取OpenAI API密钥")
    print("-" * 40)

    print("🔑 **OpenAI API密钥获取指南**:")
    print("1. 访问: https://platform.openai.com/api-keys")
    print("2. 注册/登录您的OpenAI账户")
    print("3. 点击 'Create new secret key'")
    print("4. 给密钥命名 (如: FigureYa-RAG)")
    print("5. 复制生成的密钥")
    print("6. 建议充值 $5-10 测试")

    # 询问是否需要打开网页
    open_web = input("\n🌐 是否打开OpenAI API密钥页面? (Y/n): ").strip().lower()
    if open_web != 'n':
        try:
            webbrowser.open("https://platform.openai.com/api-keys")
            print("✅ 已在浏览器中打开API密钥页面")
        except:
            print("❌ 无法打开浏览器，请手动访问: https://platform.openai.com/api-keys")

    print("\n💡 **API密钥格式**: sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("⚠️  请妥善保管API密钥，不要分享给他人")

    return input("\n🔑 请输入您的OpenAI API密钥: ").strip()

def validate_api_key(api_key):
    """验证API密钥格式"""
    if not api_key:
        print("❌ API密钥不能为空")
        return False

    if not api_key.startswith("sk-"):
        print("⚠️  OpenAI API密钥通常以 'sk-' 开头")
        confirm = input("确定要继续吗? (y/N): ").strip().lower()
        return confirm == 'y'

    if len(api_key) < 20:
        print("⚠️  API密钥长度似乎太短")
        confirm = input("确定要继续吗? (y/N): ").strip().lower()
        return confirm == 'y'

    return True

def step2_install_dependencies():
    """步骤2: 安装依赖"""
    print("\n📋 步骤 2/4: 检查和安装依赖包")
    print("-" * 40)

    required_packages = ["openai", "numpy", "requests"]

    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"📥 正在安装 {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"✅ {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"❌ {package} 安装失败")
                print(f"💡 请手动运行: pip install {package}")
                return False

    return True

def step3_save_api_key(api_key):
    """步骤3: 保存API密钥"""
    print("\n📋 步骤 3/4: 保存API密钥配置")
    print("-" * 40)

    # 读取现有.env文件
    env_path = Path(".env")
    lines = []
    if env_path.exists():
        with open(env_path, 'r') as f:
            lines = f.readlines()

    # 更新API密钥
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
    print(f"🔒 密钥已安全存储 (仅显示前10位): {api_key[:10]}...")

    return True

def step4_test_connection(api_key):
    """步骤4: 测试API连接"""
    print("\n📋 步骤 4/4: 测试API连接")
    print("-" * 40)

    try:
        import openai

        print("🔍 正在测试OpenAI API连接...")
        print("   (这可能需要几秒钟)")

        # 创建客户端
        client = openai.OpenAI(api_key=api_key)

        # 发送测试请求
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个生物医学数据分析专家。"},
                {"role": "user", "content": "请回复'API连接测试成功'"}
            ],
            max_tokens=10,
            timeout=30
        )

        result = response.choices[0].message.content.strip()
        print("✅ API连接测试成功!")
        print(f"💬 GPT回复: {result}")
        print("🎉 您的API密钥配置完成!")

        return True

    except openai.AuthenticationError:
        print("❌ API密钥认证失败")
        print("💡 请检查:")
        print("   • API密钥是否正确")
        print("   • 密钥是否已激活")
        print("   • 账户是否有余额")
        return False

    except openai.RateLimitError:
        print("❌ API请求频率限制")
        print("💡 请稍后再试或检查账户余额")
        return False

    except openai.APIConnectionError:
        print("❌ 网络连接问题")
        print("💡 请检查网络连接")
        return False

    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def show_success_screen():
    """显示成功界面"""
    print("\n" + "="*60)
    print("🎉 恭喜! FigureYa 智能RAG系统配置完成!")
    print("="*60)

    print("\n🚀 **现在您可以体验真正的AI功能**:")
    print("   • 语义搜索 (不是关键词匹配)")
    print("   • GPT-3.5生成的专业回答")
    print("   • 上下文理解和推理")
    print("   • 个性化生物医学分析建议")
    print("   • 高置信度 (0.85-0.95) 的智能回答")

    print("\n🎯 **立即开始使用**:")
    print("   方法1: python3 smart_figureya_rag.py")
    print("   方法2: source .env && python3 smart_figureya_rag.py")
    print("   方法3: python3 figureya_rag_server_fixed.py")

    print("\n💡 **功能对比**:")
    print("   基础版本: 关键词匹配，模板化回答")
    print("   AI版本: 语义理解，GPT生成个性化建议")

    print("\n📊 **预期体验**:")
    print("   🧠 真正的生物医学专家级分析")
    print("   📊 个性化的方法学建议")
    print("   🔬 专业的结果解读指导")
    print("   💡 智能的参数优化建议")

    choice = input("\n🎯 是否现在运行智能RAG系统? (Y/n): ").strip().lower()

    if choice != 'n':
        print("\n🚀 启动智能RAG系统...")
        try:
            subprocess.run([sys.executable, "smart_figureya_rag.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ 启动失败，请检查配置")
            print("💡 您可以手动运行: python3 smart_figureya_rag.py")

def main():
    """主流程"""
    print_header()

    # 步骤1: 获取API密钥
    api_key = step1_get_api_key()

    if not validate_api_key(api_key):
        print("❌ API密钥验证失败，配置中止")
        return

    # 步骤2: 安装依赖
    if not step2_install_dependencies():
        print("❌ 依赖安装失败，请手动安装后重试")
        return

    # 步骤3: 保存API密钥
    if not step3_save_api_key(api_key):
        print("❌ API密钥保存失败")
        return

    # 步骤4: 测试连接
    if not step4_test_connection(api_key):
        print("❌ API连接测试失败")
        retry = input("是否重新配置? (y/N): ").strip().lower()
        if retry == 'y':
            main()
        return

    # 显示成功界面
    show_success_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 配置已取消")
    except Exception as e:
        print(f"\n❌ 配置过程中出现错误: {e}")
        print("💡 您可以使用基础版本: python3 demo_smart_rag.py")