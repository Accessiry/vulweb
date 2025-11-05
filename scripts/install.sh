#!/bin/bash
# VulWeb 系统安装脚本 (WSL/Ubuntu)

set -e

echo "========================================="
echo "  VulWeb 系统环境安装"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 更新系统
echo -e "${YELLOW}[1/5] 更新系统包...${NC}"
sudo apt-get update

# 安装Python和相关工具
echo -e "${YELLOW}[2/5] 安装Python环境...${NC}"
sudo apt-get install -y python3 python3-pip python3-venv

# 安装Node.js (使用NodeSource仓库获取最新版本)
echo -e "${YELLOW}[3/5] 安装Node.js环境...${NC}"
if ! command -v node &> /dev/null; then
    # 安装Node.js 18.x
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo -e "${GREEN}Node.js 已安装，跳过${NC}"
fi

# 验证安装
echo -e "${YELLOW}[4/5] 验证安装...${NC}"
echo "Python版本: $(python3 --version)"
echo "pip版本: $(pip3 --version)"
echo "Node.js版本: $(node --version)"
echo "npm版本: $(npm --version)"

# 创建必要的目录
echo -e "${YELLOW}[5/5] 创建项目目录...${NC}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/models"
mkdir -p "$PROJECT_ROOT/datasets"
mkdir -p "$PROJECT_ROOT/backend/uploads/models"
mkdir -p "$PROJECT_ROOT/backend/uploads/datasets"
mkdir -p "$PROJECT_ROOT/backend/training_outputs"

# 设置脚本执行权限
chmod +x "$SCRIPT_DIR"/*.sh

echo ""
echo "========================================="
echo "  环境安装完成！"
echo "========================================="
echo ""
echo "下一步:"
echo "  1. 安装Python依赖: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo "  2. 安装Node.js依赖: cd frontend && npm install"
echo "  3. 启动系统: ./scripts/start.sh"
echo ""
