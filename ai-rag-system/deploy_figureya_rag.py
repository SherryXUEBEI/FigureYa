#!/usr/bin/env python3
"""
FigureYa RAG 系统部署脚本
快速启动Web界面和API服务
"""

import os
import json
import http.server
import socketserver
import webbrowser
from pathlib import Path
import threading
import time

class FigureYaRAGDeployer:
    """FigureYa RAG部署器"""

    def __init__(self, port=8080):
        self.port = port
        self.figureya_path = Path("/Users/mypro/Downloads/FigureYa")
        self.deploy_dir = self.figureya_path / "rag_deployment"

    def prepare_deployment(self):
        """准备部署文件"""
        print("🚀 准备FigureYa RAG部署...")

        # 创建部署目录
        self.deploy_dir.mkdir(exist_ok=True)

        # 复制必要文件
        files_to_copy = [
            "figureya_rag_web.html",
            "figureya_knowledge_base.json",
            "figureya_summary_report.md",
            "FigureYa_RAG_Design.md"
        ]

        for filename in files_to_copy:
            src = self.figureya_path / filename
            dst = self.deploy_dir / filename
            if src.exists():
                if src.is_file():
                    dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
                    print(f"✅ 复制文件: {filename}")
                else:
                    import shutil
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    print(f"✅ 复制目录: {filename}")
            else:
                print(f"⚠️ 文件不存在: {filename}")

        # 创建index.html（重定向到主页面）
        index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=figureya_rag_web.html">
    <title>FigureYa RAG - 智能生物医学分析助手</title>
</head>
<body>
    <p>正在跳转到FigureYa RAG智能助手...</p>
</body>
</html>"""
        (self.deploy_dir / "index.html").write_text(index_html, encoding='utf-8')

        print(f"✅ 部署文件准备完成: {self.deploy_dir}")

    def create_api_server(self):
        """创建简单的API服务器"""
        api_code = '''#!/usr/bin/env python3
"""
FigureYa RAG API服务
提供RESTful API接口
"""

import json
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from figureya_rag_processor import FigureYaRAGProcessor
from figureya_rag_chat import FigureYaRAGChat

class FigureYaRAGAPI(BaseHTTPRequestHandler):
    """FigureYa RAG API处理器"""

    def __init__(self, *args, **kwargs):
        self.rag_system = None
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/':
            self.serve_file('figureya_rag_web.html')
        elif parsed_path.path == '/api/status':
            self.handle_status()
        elif parsed_path.path.startswith('/api/search'):
            self.handle_search(parsed_path)
        else:
            self.serve_file(parsed_path.path.lstrip('/'))

    def do_POST(self):
        """处理POST请求"""
        parsed_path = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        if parsed_path.path == '/api/chat':
            self.handle_chat(post_data)
        else:
            self.send_error(404)

    def handle_status(self):
        """处理状态查询"""
        response = {
            "status": "ready",
            "modules_count": 348,
            "version": "1.0.0",
            "features": [
                "模块推荐",
                "参数帮助",
                "数据准备指导",
                "结果解读"
            ]
        }
        self.send_json_response(response)

    def handle_search(self, parsed_path):
        """处理搜索请求"""
        query_params = parse_qs(parsed_path.query)
        query = query_params.get('q', [''])[0]
        limit = int(query_params.get('limit', [5])[0])

        if not self.rag_system:
            self.rag_system = FigureYaRAGChat("/Users/mypro/Downloads/FigureYa")

        results = self.rag_system.processor.search_modules(query, top_k=limit)

        response = {
            "query": query,
            "results": results,
            "count": len(results)
        }
        self.send_json_response(response)

    def handle_chat(self, post_data):
        """处理聊天请求"""
        try:
            data = json.loads(post_data.decode('utf-8'))
            query = data.get('message', '')

            if not self.rag_system:
                self.rag_system = FigureYaRAGChat("/Users/mypro/Downloads/FigureYa")

            response = self.rag_system.chat(query)
            self.send_json_response(response)

        except Exception as e:
            error_response = {"error": str(e)}
            self.send_json_response(error_response, status=500)

    def serve_file(self, filename):
        """提供静态文件服务"""
        file_path = Path(__file__).parent / filename
        if file_path.exists() and file_path.is_file():
            self.send_response(200)
            self.send_header('Content-type', self.get_content_type(filename))
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def send_json_response(self, data, status=200):
        """发送JSON响应"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response_json = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response_json.encode('utf-8'))

    def get_content_type(self, filename):
        """获取文件内容类型"""
        if filename.endswith('.html'):
            return 'text/html'
        elif filename.endswith('.css'):
            return 'text/css'
        elif filename.endswith('.js'):
            return 'application/javascript'
        elif filename.endswith('.json'):
            return 'application/json'
        else:
            return 'text/plain'

    def log_message(self, format, *args):
        """自定义日志格式"""
        pass  # 静默日志输出

def main():
    """启动API服务器"""
    port = 8081
    server = HTTPServer(('localhost', port), FigureYaRAGAPI)
    print(f"🚀 FigureYa RAG API服务启动: http://localhost:{port}")
    print("📚 API端点:")
    print("   GET  /api/status - 系统状态")
    print("   GET  /api/search?q=查询词 - 搜索模块")
    print("   POST /api/chat - 智能对话")
    print("   按 Ctrl+C 停止服务")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n👋 API服务已停止")
        server.shutdown()

if __name__ == "__main__":
    main()
'''

        api_file = self.deploy_dir / "api_server.py"
        api_file.write_text(api_code, encoding='utf-8')
        api_file.chmod(0o755)  # 设置执行权限

        print("✅ API服务器文件创建完成")

    def start_web_server(self):
        """启动Web服务器"""
        print(f"🌐 启动Web服务器: http://localhost:{self.port}")

        # 切换到部署目录
        os.chdir(self.deploy_dir)

        # 创建HTTP服务器
        handler = http.server.SimpleHTTPRequestHandler

        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                print(f"✅ Web服务器运行在: http://localhost:{self.port}")
                print("📱 访问地址进行体验")
                print("🛑 按 Ctrl+C 停止服务器")

                # 自动打开浏览器
                webbrowser.open(f"http://localhost:{self.port}")

                # 启动服务器
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\n👋 Web服务器已停止")
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"⚠️ 端口 {self.port} 已被占用，尝试使用端口 {self.port + 1}")
                self.port = self.port + 1
                self.start_web_server()
            else:
                print(f"❌ 启动服务器失败: {e}")

    def start_api_server(self):
        """启动API服务器（后台运行）"""
        def run_api():
            os.chdir(self.deploy_dir)
            import subprocess
            subprocess.run([sys.executable, "api_server.py"])

        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()
        time.sleep(2)  # 等待API服务器启动
        print("✅ API服务器已启动: http://localhost:8081")

    def deploy(self):
        """完整部署流程"""
        print("🎯 FigureYa RAG 智能生物医学分析助手")
        print("=" * 50)

        # 准备部署文件
        self.prepare_deployment()

        # 创建API服务器
        self.create_api_server()

        print("\\n🚀 启动服务...")
        print("-" * 30)

        # 启动API服务器（后台）
        self.start_api_server()

        # 启动Web服务器（前台）
        self.start_web_server()

    def create_startup_script(self):
        """创建启动脚本"""
        startup_script = f'''#!/bin/bash
# FigureYa RAG 启动脚本

echo "🚀 启动 FigureYa RAG 智能助手..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 切换到部署目录
cd "{self.deploy_dir}"

# 启动服务
echo "🌐 Web界面: http://localhost:8080"
echo "🔧 API服务: http://localhost:8081"
echo "📖 文档: {self.deploy_dir}/FigureYa_RAG_Design.md"
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
'''

        startup_file = self.deploy_dir / "start_rag.sh"
        startup_file.write_text(startup_script, encoding='utf-8')
        startup_file.chmod(0o755)

        print("✅ 启动脚本创建完成")


def main():
    """主函数"""
    import sys

    print("🎯 FigureYa RAG 部署工具")
    print("=" * 40)

    deployer = FigureYaRAGDeployer()

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "prepare":
            deployer.prepare_deployment()
            deployer.create_api_server()
            deployer.create_startup_script()
            print("\\n✅ 部署准备完成！")
            print(f"📁 部署目录: {deployer.deploy_dir}")
            print("🚀 运行以下命令启动服务:")
            print(f"   cd {deployer.deploy_dir}")
            print("   ./start_rag.sh")
        elif command == "start":
            deployer.deploy()
        else:
            print("未知命令。使用 'prepare' 或 'start'")
    else:
        # 直接启动完整部署
        deployer.deploy()


if __name__ == "__main__":
    main()