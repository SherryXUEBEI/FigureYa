# 🔧 FigureYa RAG 故障排除指南

## 🚨 常见问题及解决方案

### 1. SIGPIPE信号错误

**问题描述**：
```
An error has occurred!
ignoring SIGPIPE signal
```

**原因**：
- 客户端（浏览器）断开连接时，服务器仍在尝试写入数据
- 在Unix/Linux系统中，当管道的读端关闭时，写端会收到SIGPIPE信号

**解决方案**：
- ✅ 已在修复版本中处理：`signal.signal(signal.SIGPIPE, signal.SIG_DFL)`
- ✅ 使用异常处理：`try/except BrokenPipeError, ConnectionResetError`

**使用修复版本**：
```bash
python3 figureya_rag_server_fixed.py
# 或使用启动脚本
./start_figureya_rag.sh
```

### 2. 端口占用错误

**问题描述**：
```
OSError: [Errno 48] Address already in use
```

**解决方案**：
```bash
# 查找占用端口的进程
lsof -i :8080

# 停止占用进程
kill -9 <PID>

# 或使用自动端口检测
./start_figureya_rag.sh  # 会自动寻找可用端口
```

### 3. 内存不足错误

**问题描述**：
```
MemoryError: Unable to allocate array
```

**原因**：
- 同时处理过多文本文件
- 知识库数据量过大

**解决方案**：
- ✅ 修复版本已限制处理文件数量（最多200个）
- ✅ 分批处理，避免内存溢出
```python
# 在figureya_rag_processor_fixed.py中
max_files = min(len(text_files), 200)
```

### 4. 编码错误

**问题描述**：
```
UnicodeDecodeError: 'utf-8' codec can't decode
```

**解决方案**：
- ✅ 修复版本支持多种编码尝试
```python
try:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    try:
        with open(file, 'r', encoding='gbk') as f:
            content = f.read()
    except:
        content = file.read_text(encoding='utf-8', errors='ignore')
```

### 5. 网络连接问题

**问题描述**：
- 浏览器无法连接到服务器
- API请求超时

**解决方案**：
```bash
# 检查服务器状态
curl http://localhost:8080/api/status

# 检查网络连接
telnet localhost 8080

# 重启服务器
./start_figureya_rag.sh
```

### 6. 知识库加载失败

**问题描述**：
```
❌ 无法加载知识库，程序退出
```

**解决方案**：
```bash
# 1. 检查文件路径
ls -la texts/  # 确认texts目录存在

# 2. 重新生成知识库
python3 figureya_rag_processor_fixed.py

# 3. 检查权限
chmod -R 755 texts/
```

### 7. 浏览器兼容性问题

**问题描述**：
- 某些浏览器功能不正常
- JavaScript错误

**解决方案**：
- ✅ 使用现代浏览器：Chrome, Firefox, Safari, Edge
- ✅ 清除浏览器缓存
- ✅ 检查浏览器控制台错误信息

**推荐浏览器**：
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🛠️ 调试工具

### 1. 服务器状态检查
```bash
# 检查API状态
curl http://localhost:8080/api/status

# 检查健康状态
curl http://localhost:8080/api/health

# 测试搜索功能
curl "http://localhost:8080/api/search?q=RNA-seq"
```

### 2. 日志分析
```bash
# 查看系统日志
tail -f /var/log/system.log

# 查看Python错误日志
python3 figureya_rag_server_fixed.py 2>&1 | tee server.log
```

### 3. 网络诊断
```bash
# 检查端口监听
netstat -an | grep 8080

# 检查进程
ps aux | grep figureya_rag

# 检查连接数
netstat -an | grep ESTABLISHED | wc -l
```

## 🔄 恢复程序

### 完全重置
```bash
# 1. 停止所有相关进程
pkill -f figureya_rag

# 2. 清理临时文件
rm -f figureya_knowledge_base.json
rm -f server.log
rm -f figureya_summary_report_fixed.md

# 3. 重新启动
./start_figureya_rag.sh
```

### 备份重要文件
```bash
# 备份知识库
cp figureya_knowledge_base.json figureya_knowledge_base_backup.json

# 备份配置
cp start_figureya_rag.sh start_figureya_rag_backup.sh
```

## 📞 技术支持

### 自助诊断清单
在报告问题前，请确认以下项目：

- [ ] Python版本 >= 3.7
- [ ] 所有依赖文件存在
- [ ] 端口8080未被占用
- [ ] 防火墙允许本地连接
- [] 浏览器版本支持
- [ ] 磁盘空间充足 (>100MB)
- [ ] 内存充足 (>512MB)

### 收集诊断信息
```bash
# 创建诊断报告
cat > diagnosis.txt << EOF
FigureYa RAG 诊断报告
=====================

系统信息:
$(uname -a)

Python版本:
$(python3 --version)

磁盘空间:
$(df -h .)

内存使用:
$(free -h)

网络状态:
$(netstat -an | grep 8080)

进程状态:
$(ps aux | grep figureya_rag)

当前目录:
$(pwd)

文件列表:
$(ls -la)

错误日志:
$(tail -20 server.log 2>/dev/null || echo "无日志文件")
EOF

echo "诊断报告已生成: diagnosis.txt"
```

### 常用修复命令
```bash
# 修复权限
chmod +x *.sh
chmod -R 755 texts/

# 修复依赖
pip3 install --upgrade setuptools wheel

# 清理缓存
python3 -m pip cache purge

# 重新安装依赖（如果需要）
pip3 install -r requirements.txt  # 如果存在
```

## 🚀 性能优化

### 内存优化
- 限制同时处理的文件数量
- 使用生成器而非列表
- 及时释放不需要的对象

### 网络优化
- 设置合理的超时时间
- 限制请求大小
- 启用gzip压缩

### 并发优化
- 使用线程池处理请求
- 异步处理长时间任务
- 限制并发连接数

## 📈 监控指标

### 关键指标
- CPU使用率 < 80%
- 内存使用率 < 70%
- 响应时间 < 2秒
- 错误率 < 1%

### 监控命令
```bash
# 监控系统资源
htop

# 监控网络连接
ss -tuln

# 监控磁盘I/O
iotop

# 监控进程状态
watch -n 1 'ps aux | grep figureya_rag'
```

---

**提示**：大多数问题都可以通过重新启动服务解决。如果问题持续存在，请查看日志文件并收集诊断信息。