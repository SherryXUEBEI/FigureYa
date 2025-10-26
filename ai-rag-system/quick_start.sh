#!/bin/bash

echo "🧠 FigureYa AI RAG系统 - 快速启动脚本"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

echo "✅ Python3环境检查通过"

# 检查API密钥配置
if [ -f ".env" ]; then
    echo "✅ 找到.env配置文件"
    source .env
else
    echo "📝 未找到.env文件，使用模板创建..."
    cp .env.example .env
    echo "⚠️  请编辑.env文件并填入您的API密钥"
    echo "   智谱AI: https://bigmodel.cn/usercenter/proj-mgmt/apikeys"
    echo "   OpenAI: https://platform.openai.com/api-keys"
fi

# 选择启动模式
echo ""
echo "🚀 请选择启动模式:"
echo "1. 智谱AI版本 (推荐)"
echo "2. OpenAI版本"
echo "3. 基础演示版本 (无需API)"
echo "4. Web界面版本"
echo "5. GitHub Pages演示"

read -p "请输入选择 (1-5): " choice

case $choice in
    1)
        echo "🤖 启动智谱AI版本..."
        if [ -n "$ZHIPUAI_API_KEY" ] && [ "$ZHIPUAI_API_KEY" != "your-zhipuai-api-key-here" ]; then
            python3 zhipuai_rag_system.py
        else
            echo "❌ 未配置智谱AI API密钥"
            echo "💡 请编辑.env文件或运行: python3 quick_zhipuai_setup.py"
        fi
        ;;
    2)
        echo "🧠 启动OpenAI版本..."
        if [ -n "$OPENAI_API_KEY" ] && [ "$OPENAI_API_KEY" != "your-openai-api-key-here" ]; then
            python3 smart_figureya_rag.py
        else
            echo "❌ 未配置OpenAI API密钥"
            echo "💡 请编辑.env文件或运行: python3 quick_setup.py"
        fi
        ;;
    3)
        echo "🎭 启动基础演示版本..."
        python3 demo_smart_rag.py
        ;;
    4)
        echo "🌐 启动Web界面版本..."
        python3 github_pages_rag_backend.py --mock --port 8080
        ;;
    5)
        echo "📱 打开GitHub Pages演示..."
        if command -v open &> /dev/null; then
            open figureya_ai_search_public.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open figureya_ai_search_public.html
        else
            echo "请手动打开: figureya_ai_search_public.html"
        fi
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac