#!/bin/bash
# VulWeb 系统验证脚本
# 验证系统是否正确安装和配置

set -e

echo "========================================="
echo "  VulWeb 系统验证"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# 检查Python
echo -n "检查 Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ 未安装${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 检查Node.js
echo -n "检查 Node.js... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ 未安装${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 检查npm
echo -n "检查 npm... "
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ v$NPM_VERSION${NC}"
else
    echo -e "${RED}✗ 未安装${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 检查目录结构
echo -n "检查项目目录... "
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ -d "$PROJECT_ROOT/backend" ] && [ -d "$PROJECT_ROOT/frontend" ]; then
    echo -e "${GREEN}✓ 正确${NC}"
else
    echo -e "${RED}✗ 目录缺失${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 检查后端依赖文件
echo -n "检查后端依赖文件... "
if [ -f "$PROJECT_ROOT/backend/requirements.txt" ]; then
    echo -e "${GREEN}✓ 存在${NC}"
else
    echo -e "${RED}✗ 缺失${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 检查前端依赖文件
echo -n "检查前端依赖文件... "
if [ -f "$PROJECT_ROOT/frontend/package.json" ]; then
    echo -e "${GREEN}✓ 存在${NC}"
else
    echo -e "${RED}✗ 缺失${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 检查配置文件
echo -n "检查配置文件... "
if [ -f "$PROJECT_ROOT/config/config.ini" ]; then
    echo -e "${GREEN}✓ 存在${NC}"
else
    echo -e "${YELLOW}⚠ 未找到（可选）${NC}"
fi

# 检查Python虚拟环境
echo -n "检查Python虚拟环境... "
if [ -d "$PROJECT_ROOT/backend/venv" ]; then
    echo -e "${GREEN}✓ 已创建${NC}"
else
    echo -e "${YELLOW}⚠ 未创建（运行时需要）${NC}"
fi

# 检查Node模块
echo -n "检查Node模块... "
if [ -d "$PROJECT_ROOT/frontend/node_modules" ]; then
    echo -e "${GREEN}✓ 已安装${NC}"
else
    echo -e "${YELLOW}⚠ 未安装（运行时需要）${NC}"
fi

# 检查必要目录
echo -n "检查必要目录... "
ALL_DIRS_EXIST=true
for dir in logs models datasets scripts docs config; do
    if [ ! -d "$PROJECT_ROOT/$dir" ]; then
        ALL_DIRS_EXIST=false
        break
    fi
done

if [ "$ALL_DIRS_EXIST" = true ]; then
    echo -e "${GREEN}✓ 完整${NC}"
else
    echo -e "${RED}✗ 部分目录缺失${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 检查脚本权限
echo -n "检查脚本执行权限... "
if [ -x "$SCRIPT_DIR/start.sh" ] && [ -x "$SCRIPT_DIR/stop.sh" ]; then
    echo -e "${GREEN}✓ 正确${NC}"
else
    echo -e "${YELLOW}⚠ 需要设置（运行: chmod +x scripts/*.sh）${NC}"
fi

# 检查端口占用
echo -n "检查端口 5000... "
if ! netstat -tuln 2>/dev/null | grep -q ":5000 " && ! ss -tuln 2>/dev/null | grep -q ":5000 "; then
    echo -e "${GREEN}✓ 可用${NC}"
else
    echo -e "${YELLOW}⚠ 已占用${NC}"
fi

echo -n "检查端口 3000... "
if ! netstat -tuln 2>/dev/null | grep -q ":3000 " && ! ss -tuln 2>/dev/null | grep -q ":3000 "; then
    echo -e "${GREEN}✓ 可用${NC}"
else
    echo -e "${YELLOW}⚠ 已占用${NC}"
fi

# 总结
echo ""
echo "========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ 系统验证通过${NC}"
    echo ""
    echo "下一步:"
    echo "1. 安装依赖:"
    echo "   cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cd .."
    echo "   cd frontend && npm install && cd .."
    echo ""
    echo "2. 启动系统:"
    echo "   ./scripts/start.sh"
    echo ""
else
    echo -e "${RED}✗ 发现 $ERRORS 个问题${NC}"
    echo ""
    echo "请先解决上述问题，然后重新运行此脚本"
fi
echo "========================================="
echo ""
