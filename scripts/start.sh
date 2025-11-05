#!/bin/bash
# VulWeb 系统启动脚本 (WSL/Linux)
# 一键启动前后端服务

set -e

echo "========================================="
echo "  VulWeb 代码漏洞检测模型管理系统"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}项目根目录: $PROJECT_ROOT${NC}"
echo ""

# 检查Python
echo -e "${YELLOW}[1/6] 检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3 未安装"
    echo "请运行: sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi
echo -e "${GREEN}✓ Python3 已安装${NC}"

# 检查Node.js
echo -e "${YELLOW}[2/6] 检查Node.js环境...${NC}"
if ! command -v node &> /dev/null; then
    echo "错误: Node.js 未安装"
    echo "请运行安装脚本中的Node.js安装步骤"
    exit 1
fi
echo -e "${GREEN}✓ Node.js 已安装${NC}"

# 启动后端
echo -e "${YELLOW}[3/6] 启动后端服务...${NC}"
cd "$PROJECT_ROOT/backend"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖（如果需要）
if [ ! -f "venv/.deps_installed" ]; then
    echo "安装Python依赖..."
    pip install -r requirements.txt
    touch venv/.deps_installed
fi

# 创建必要的目录
mkdir -p uploads/models uploads/datasets training_outputs

# 启动后端服务（后台运行）
echo "启动Flask后端..."
python run.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
echo -e "${GREEN}✓ 后端服务已启动 (PID: $BACKEND_PID)${NC}"

# 等待后端启动
sleep 3

# 启动前端
echo -e "${YELLOW}[4/6] 启动前端服务...${NC}"
cd "$PROJECT_ROOT/frontend"

# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo "安装Node.js依赖..."
    npm install
fi

# 启动前端服务（后台运行）
echo "启动Vue.js前端..."
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
echo -e "${GREEN}✓ 前端服务已启动 (PID: $FRONTEND_PID)${NC}"

# 等待服务启动
echo -e "${YELLOW}[5/6] 等待服务启动...${NC}"
sleep 5

# 检查服务状态
echo -e "${YELLOW}[6/6] 检查服务状态...${NC}"

# 检查后端
if curl -s http://localhost:5000/health > /dev/null; then
    echo -e "${GREEN}✓ 后端服务运行正常 (http://localhost:5000)${NC}"
else
    echo -e "${YELLOW}⚠ 后端服务可能还在启动中...${NC}"
fi

# 检查前端
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✓ 前端服务运行正常 (http://localhost:3000)${NC}"
else
    echo -e "${YELLOW}⚠ 前端服务可能还在启动中...${NC}"
fi

echo ""
echo "========================================="
echo "  服务启动完成！"
echo "========================================="
echo ""
echo "访问地址:"
echo "  - 前端: http://localhost:3000"
echo "  - 后端API: http://localhost:5000"
echo ""
echo "停止服务:"
echo "  ./scripts/stop.sh"
echo ""
echo "查看日志:"
echo "  tail -f logs/backend.log"
echo "  tail -f logs/frontend.log"
echo ""
