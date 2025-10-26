#!/bin/bash
# FigureYa RAG 启动脚本

echo "🚀 启动 FigureYa RAG 智能助手..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 切换到部署目录
cd "/Users/mypro/Downloads/FigureYa/rag_deployment"

# 启动服务
echo "🌐 Web界面: http://localhost:8080"
echo "🔧 API服务: http://localhost:8081"
echo "📖 文档: /Users/mypro/Downloads/FigureYa/rag_deployment/FigureYa_RAG_Design.md"
echo ""
echo "按任意键启动服务..."
read -n 1

# 同时启动Web和API服务
python3 api_server.py &
API_PID=$!

sleep 2

echo "✅ 服务已启动！"
echo "📱 打开浏览器访问: http://localhost:8080"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待中断信号
trap "kill $API_PID; exit" INT
wait
