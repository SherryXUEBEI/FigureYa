#!/bin/bash

# FigureYa RAG 智能生物医学分析助手启动脚本

echo "🧠 FigureYa RAG 智能生物医学分析助手"
echo "=========================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    echo "安装方法："
    echo "  macOS: brew install python3"
    echo "  Ubuntu: sudo apt-get install python3"
    exit 1
fi

echo "✅ Python3环境检查通过"

# 检查必要文件
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 当前目录: $CURRENT_DIR"

# 检查关键文件
REQUIRED_FILES=(
    "figureya_rag_processor_fixed.py"
    "figureya_rag_server_fixed.py"
    "figureya_rag_web.html"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$CURRENT_DIR/$file" ]]; then
        echo "❌ 缺少必要文件: $file"
        exit 1
    fi
done

echo "✅ 必要文件检查通过"

# 设置信号处理
cleanup() {
    echo ""
    echo "👋 正在停止服务..."

    # 查找并停止相关进程
    pkill -f "figureya_rag_server" 2>/dev/null
    pkill -f "python3.*figureya_rag" 2>/dev/null

    echo "✅ 服务已停止"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 预处理知识库（如果需要）
if [[ ! -f "$CURRENT_DIR/figureya_knowledge_base.json" ]]; then
    echo "📚 首次运行，正在预处理知识库..."
    cd "$CURRENT_DIR"
    python3 figureya_rag_processor_fixed.py
    if [[ $? -ne 0 ]]; then
        echo "❌ 知识库预处理失败"
        exit 1
    fi
    echo "✅ 知识库预处理完成"
fi

# 查找可用端口
find_available_port() {
    local port=$1
    while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; do
        echo "⚠️ 端口 $port 被占用，尝试下一个端口..."
        ((port++))
        if [[ $port -gt 8090 ]]; then
            echo "❌ 无法找到可用端口"
            exit 1
        fi
    done
    echo $port
}

# 查找可用端口
PORT=$(find_available_port 8080)
echo "🔌 使用端口: $PORT"

# 启动服务器
echo ""
echo "🚀 启动FigureYa RAG服务器..."
echo "🌐 Web界面: http://localhost:$PORT"
echo "🔧 API服务: http://localhost:$PORT/api"
echo "📊 状态查询: http://localhost:$PORT/api/status"
echo ""
echo "提示："
echo "  • 在浏览器中打开上述地址开始使用"
echo "  • 按 Ctrl+C 停止服务"
echo "  • 首次访问可能需要几秒钟加载"
echo ""

# 切换到当前目录
cd "$CURRENT_DIR"

# 启动服务器
python3 figureya_rag_server_fixed.py --host localhost --port $PORT