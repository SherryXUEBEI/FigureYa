#!/usr/bin/env python3
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
        print("\n👋 API服务已停止")
        server.shutdown()

if __name__ == "__main__":
    main()
