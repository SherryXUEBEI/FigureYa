#!/usr/bin/env python3
"""
FigureYa RAG Web服务器 - 修复版本
处理SIGPIPE和其他网络问题
"""

import json
import os
import sys
import signal
import threading
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import time

# 修复SIGPIPE信号问题
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
# 忽略SIGINT信号，让主程序处理
signal.signal(signal.SIGINT, signal.SIG_DFL)

class FigureYaRAGHandler(BaseHTTPRequestHandler):
    """FigureYa RAG HTTP请求处理器"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # rag_system将通过类变量传递

    def do_GET(self):
        """处理GET请求"""
        try:
            parsed_path = urlparse(self.path)

            if parsed_path.path == '/':
                self.serve_file('figureya_rag_web.html')
            elif parsed_path.path == '/api/status':
                self.handle_status()
            elif parsed_path.path.startswith('/api/search'):
                self.handle_search(parsed_path)
            elif parsed_path.path.startswith('/api/health'):
                self.handle_health()
            else:
                # 尝试提供静态文件
                self.serve_static_file(parsed_path.path.lstrip('/'))

        except ConnectionResetError:
            # 客户端断开连接，忽略
            pass
        except BrokenPipeError:
            # 管道断开，忽略
            pass
        except Exception as e:
            self.log_error(f"处理GET请求时出错: {e}")
            self.send_error(500, "Internal Server Error")

    def do_POST(self):
        """处理POST请求"""
        try:
            parsed_path = urlparse(self.path)
            content_length = int(self.headers.get('Content-Length', 0))

            # 限制读取大小以防止内存问题
            max_content_length = 1024 * 1024  # 1MB
            if content_length > max_content_length:
                self.send_error(413, "Request Entity Too Large")
                return

            post_data = b''
            remaining = content_length
            while remaining > 0:
                chunk_size = min(4096, remaining)
                try:
                    chunk = self.rfile.read(chunk_size)
                    if not chunk:
                        break
                    post_data += chunk
                    remaining -= len(chunk)
                except ConnectionResetError:
                    break
                except BrokenPipeError:
                    break

            if parsed_path.path == '/api/chat':
                self.handle_chat(post_data)
            elif parsed_path.path == '/api/analyze':
                self.handle_analyze(post_data)
            else:
                self.send_error(404)

        except ConnectionResetError:
            pass
        except BrokenPipeError:
            pass
        except Exception as e:
            self.log_error(f"处理POST请求时出错: {e}")
            self.send_error(500, "Internal Server Error")

    def handle_status(self):
        """处理状态查询"""
        try:
            rag_system = getattr(self.__class__, 'rag_system', None)
            status_data = {
                "status": "ready",
                "timestamp": int(time.time()),
                "modules_count": len(rag_system.knowledge_base) if rag_system else 0,
                "version": "1.0.0",
                "features": [
                    "模块推荐",
                    "参数帮助",
                    "数据准备指导",
                    "结果解读"
                ]
            }
            self.send_json_response(status_data)
        except Exception as e:
            self.log_error(f"处理状态查询时出错: {e}")
            self.send_error(500)

    def handle_health(self):
        """处理健康检查"""
        try:
            start_time = getattr(self.__class__, 'start_time', time.time())
            health_data = {
                "status": "healthy",
                "timestamp": int(time.time()),
                "uptime": time.time() - start_time
            }
            self.send_json_response(health_data)
        except Exception as e:
            self.log_error(f"处理健康检查时出错: {e}")
            self.send_error(500)

    def handle_search(self, parsed_path):
        """处理搜索请求"""
        try:
            query_params = parse_qs(parsed_path.query)
            query = query_params.get('q', [''])[0]
            limit = min(int(query_params.get('limit', [5])[0]), 20)  # 限制最大返回数量

            rag_system = getattr(self.__class__, 'rag_system', None)
            if not rag_system:
                self.send_json_response({"error": "RAG system not initialized"}, 503)
                return

            if not query.strip():
                self.send_json_response({"error": "Empty query"}, 400)
                return

            # 使用处理器的搜索方法
            processor = rag_system.processor if hasattr(rag_system, 'processor') else rag_system
            results = processor.search_modules(query, top_k=limit)

            response = {
                "query": query,
                "results": results[:limit],
                "count": len(results)
            }
            self.send_json_response(response)

        except Exception as e:
            self.log_error(f"处理搜索请求时出错: {e}")
            self.send_json_response({"error": str(e)}, 500)

    def handle_chat(self, post_data):
        """处理聊天请求"""
        try:
            if not post_data:
                self.send_json_response({"error": "No data received"}, 400)
                return

            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_json_response({"error": "Invalid JSON"}, 400)
                return

            query = data.get('message', '').strip()
            if not query:
                self.send_json_response({"error": "Empty message"}, 400)
                return

            rag_system = getattr(self.__class__, 'rag_system', None)
            if not rag_system:
                # 尝试初始化RAG系统
                try:
                    from figureya_rag_processor_fixed import FigureYaRAGProcessor
                    processor = FigureYaRAGProcessor("/Users/mypro/Downloads/FigureYa")
                    knowledge_base = processor.load_knowledge_base()
                    from figureya_rag_chat import FigureYaRAGChat
                    rag_system = FigureYaRAGChat("/Users/mypro/Downloads/FigureYa")
                    self.__class__.rag_system = rag_system
                except Exception as e:
                    self.send_json_response({"error": f"Failed to initialize RAG system: {e}"}, 503)
                    return

            response = rag_system.chat(query)
            self.send_json_response(response)

        except Exception as e:
            self.log_error(f"处理聊天请求时出错: {e}")
            self.send_json_response({"error": str(e)}, 500)

    def handle_analyze(self, post_data):
        """处理数据分析请求"""
        try:
            if not post_data:
                self.send_json_response({"error": "No data received"}, 400)
                return

            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_json_response({"error": "Invalid JSON"}, 400)
                return

            # 这里可以添加数据分析逻辑
            analysis_result = {
                "status": "processed",
                "data_type": data.get('type', 'unknown'),
                "suggestions": ["建议使用差异表达分析", "考虑做质量控制"]
            }
            self.send_json_response(analysis_result)

        except Exception as e:
            self.log_error(f"处理分析请求时出错: {e}")
            self.send_json_response({"error": str(e)}, 500)

    def serve_file(self, filename):
        """提供文件服务"""
        try:
            file_path = Path(__file__).parent / filename
            if not file_path.exists():
                # 尝试在当前目录查找
                file_path = Path.cwd() / filename

            if file_path.exists() and file_path.is_file():
                self.send_response(200)
                self.send_header('Content-type', self.get_content_type(filename))
                self.send_header('Content-Length', str(file_path.stat().st_size))
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()

                try:
                    with open(file_path, 'rb') as f:
                        while True:
                            chunk = f.read(8192)
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                except (ConnectionResetError, BrokenPipeError):
                    pass
            else:
                self.send_error(404, "File not found")
        except Exception as e:
            self.log_error(f"提供文件服务时出错: {e}")
            self.send_error(500)

    def serve_static_file(self, filename):
        """提供静态文件服务"""
        try:
            # 安全检查，防止路径遍历
            if '..' in filename or filename.startswith('/'):
                self.send_error(403, "Forbidden")
                return

            # 尝试多个可能的路径
            possible_paths = [
                Path(__file__).parent / filename,
                Path.cwd() / filename,
                Path.cwd() / 'rag_deployment' / filename
            ]

            for file_path in possible_paths:
                if file_path.exists() and file_path.is_file():
                    self.send_response(200)
                    self.send_header('Content-type', self.get_content_type(filename))
                    self.send_header('Content-Length', str(file_path.stat().st_size))
                    self.send_header('Cache-Control', 'public, max-age=3600')
                    self.end_headers()

                    try:
                        with open(file_path, 'rb') as f:
                            while True:
                                chunk = f.read(8192)
                                if not chunk:
                                    break
                                self.wfile.write(chunk)
                    except (ConnectionResetError, BrokenPipeError):
                        pass
                    return

            self.send_error(404, "File not found")
        except Exception as e:
            self.log_error(f"提供静态文件服务时出错: {e}")
            self.send_error(500)

    def send_json_response(self, data, status=200):
        """发送JSON响应"""
        try:
            self.send_response(status)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            response_json = json.dumps(data, ensure_ascii=False, indent=2)
            self.wfile.write(response_json.encode('utf-8'))
        except (ConnectionResetError, BrokenPipeError):
            pass
        except Exception as e:
            self.log_error(f"发送JSON响应时出错: {e}")

    def get_content_type(self, filename):
        """获取文件内容类型"""
        content_types = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.txt': 'text/plain; charset=utf-8',
        }

        ext = Path(filename).suffix.lower()
        return content_types.get(ext, 'application/octet-stream')

    def log_message(self, format, *args):
        """自定义日志格式 - 减少日志输出"""
        # 只记录重要日志
        if 'GET /' in format % args or 'POST /api/' in format % args:
            print(f"📡 {format % args}")

    def log_error(self, message):
        """记录错误日志"""
        print(f"❌ {message}")


class FigureYaRAGServer:
    """FigureYa RAG服务器"""

    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server = None
        self.rag_system = None
        self.start_time = time.time()

    def initialize_rag_system(self):
        """初始化RAG系统"""
        try:
            print("🧠 初始化RAG系统...")
            from figureya_rag_chat import FigureYaRAGChat
            self.rag_system = FigureYaRAGChat("/Users/mypro/Downloads/FigureYa")
            print(f"✅ RAG系统初始化成功，知识库包含 {len(self.rag_system.processor.knowledge_base)} 个模块")
            return True
        except Exception as e:
            print(f"❌ RAG系统初始化失败: {e}")
            return False

    def create_handler_class(self):
        """创建处理器类"""
        class Handler(FigureYaRAGHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        # 设置类变量
        Handler.rag_system = self.rag_system
        Handler.start_time = self.start_time
        return Handler

    def start(self):
        """启动服务器"""
        try:
            # 检查端口是否被占用
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.host, self.port))
            sock.close()

            if result == 0:
                print(f"⚠️ 端口 {self.port} 已被占用，尝试使用端口 {self.port + 1}")
                self.port = self.port + 1

            # 初始化RAG系统
            if not self.initialize_rag_system():
                print("⚠️ RAG系统初始化失败，服务器将在没有RAG功能的情况下运行")

            # 创建HTTP服务器
            handler_class = self.create_handler_class()
            self.server = HTTPServer((self.host, self.port), handler_class)

            print(f"🚀 FigureYa RAG服务器启动成功!")
            print(f"🌐 Web界面: http://{self.host}:{self.port}")
            print(f"🔧 API服务: http://{self.host}:{self.port}/api")
            print(f"📊 状态查询: http://{self.host}:{self.port}/api/status")
            print("🛑 按 Ctrl+C 停止服务器")
            print("-" * 50)

            self.server.serve_forever()

        except KeyboardInterrupt:
            print("\n👋 收到停止信号，正在关闭服务器...")
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"❌ 端口 {self.port} 被占用")
            else:
                print(f"❌ 网络错误: {e}")
        except Exception as e:
            print(f"❌ 服务器启动失败: {e}")
        finally:
            self.stop()

    def stop(self):
        """停止服务器"""
        if self.server:
            try:
                self.server.shutdown()
                self.server.server_close()
                print("✅ 服务器已停止")
            except:
                pass


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='FigureYa RAG Web服务器')
    parser.add_argument('--host', default='localhost', help='服务器地址')
    parser.add_argument('--port', type=int, default=8080, help='服务器端口')
    parser.add_argument('--no-rag', action='store_true', help='不启动RAG系统')

    args = parser.parse_args()

    # 设置信号处理
    def signal_handler(signum, frame):
        print(f"\n收到信号 {signum}，正在停止服务器...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("🎯 FigureYa RAG Web服务器")
    print("=" * 40)

    server = FigureYaRAGServer(args.host, args.port)

    if not args.no_rag:
        server.initialize_rag_system()

    server.start()


if __name__ == "__main__":
    main()