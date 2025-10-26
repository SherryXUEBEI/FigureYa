#!/bin/bash

echo "🔑 FigureYa API密钥配置工具"
echo "=================================="

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "📝 创建配置文件..."
    cp .env.example .env
fi

echo ""
echo "📍 当前配置文件位置: $(pwd)/.env"
echo ""

# 显示当前API密钥状态
echo "🔍 检查API密钥状态..."

# 检查环境变量
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ 环境变量中已设置OpenAI API密钥"
    echo "   密钥预览: ${OPENAI_API_KEY:0:10}..."
    echo ""
    echo "🚀 可以直接运行智能RAG系统:"
    echo "   python3 smart_figureya_rag.py"
else
    echo "❌ 环境变量中未设置OpenAI API密钥"
    echo ""

    # 检查.env文件中的密钥
    if grep -q "your-openai-api-key-here" .env; then
        echo "⚠️  .env文件中的API密钥尚未配置"
        echo ""
        echo "🔧 请按以下步骤配置API密钥:"
        echo ""
        echo "方法1: 编辑.env文件 (推荐)"
        echo "   1. 打开文件: open .env"
        echo "   2. 修改第6行: OPENAI_API_KEY=sk-your-actual-key-here"
        echo "   3. 保存文件"
        echo ""
        echo "方法2: 设置环境变量"
        echo "   export OPENAI_API_KEY='sk-your-actual-key-here'"
        echo ""
        echo "方法3: 一次性运行"
        echo "   OPENAI_API_KEY='sk-your-actual-key-here' python3 smart_figureya_rag.py"
        echo ""
        echo "📍 获取API密钥: https://platform.openai.com/api-keys"
    else
        echo "✅ .env文件中已配置API密钥"
        echo ""
        echo "🚀 运行命令:"
        echo "   source .env && python3 smart_figureya_rag.py"
    fi
fi

echo ""
echo "💡 其他选项:"
echo "   • 查看配置文件: cat .env"
echo "   • 编辑配置文件: nano .env 或 open .env"
echo "   • 测试API密钥: python3 -c \"import os; from openai import OpenAI; client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print('✅ API连接成功' if client else '❌ 连接失败')\""