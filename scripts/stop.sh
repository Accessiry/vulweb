#!/bin/bash
# VulWeb 系统停止脚本

set -e

echo "========================================="
echo "  停止 VulWeb 服务"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取项目根目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 停止后端
if [ -f "$PROJECT_ROOT/logs/backend.pid" ]; then
    BACKEND_PID=$(cat "$PROJECT_ROOT/logs/backend.pid")
    echo -e "${YELLOW}停止后端服务 (PID: $BACKEND_PID)...${NC}"
    kill $BACKEND_PID 2>/dev/null || echo "后端进程已停止"
    rm -f "$PROJECT_ROOT/logs/backend.pid"
    echo -e "${GREEN}✓ 后端服务已停止${NC}"
else
    echo "后端PID文件不存在，跳过"
fi

# 停止前端
if [ -f "$PROJECT_ROOT/logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat "$PROJECT_ROOT/logs/frontend.pid")
    echo -e "${YELLOW}停止前端服务 (PID: $FRONTEND_PID)...${NC}"
    kill $FRONTEND_PID 2>/dev/null || echo "前端进程已停止"
    rm -f "$PROJECT_ROOT/logs/frontend.pid"
    echo -e "${GREEN}✓ 前端服务已停止${NC}"
else
    echo "前端PID文件不存在，跳过"
fi

# 清理可能残留的进程
echo -e "${YELLOW}清理残留进程...${NC}"
pkill -f "python run.py" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

echo ""
echo -e "${GREEN}所有服务已停止${NC}"
echo ""
