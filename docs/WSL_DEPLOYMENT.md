# VulWeb WSL 部署指南

本指南将帮助您在Windows WSL (Windows Subsystem for Linux) 环境中部署VulWeb系统。

## 目录

- [系统要求](#系统要求)
- [安装WSL](#安装wsl)
- [环境准备](#环境准备)
- [快速部署](#快速部署)
- [手动部署](#手动部署)
- [配置说明](#配置说明)
- [常见问题](#常见问题)

## 系统要求

- Windows 10 版本 2004 及更高版本（内部版本 19041 及更高版本）或 Windows 11
- 至少 4GB RAM
- 至少 10GB 可用磁盘空间
- 启用WSL 2

## 安装WSL

### 1. 启用WSL

以管理员身份打开PowerShell并运行：

```powershell
wsl --install
```

这将安装默认的Ubuntu发行版。如需安装其他发行版：

```powershell
# 查看可用发行版
wsl --list --online

# 安装特定发行版
wsl --install -d Ubuntu-22.04
```

### 2. 设置WSL 2

```powershell
wsl --set-default-version 2
```

### 3. 启动WSL

```powershell
wsl
```

首次启动时需要创建用户名和密码。

## 环境准备

### 1. 更新系统

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. 安装基础工具

```bash
sudo apt-get install -y git curl wget build-essential
```

## 快速部署

### 1. 克隆项目

```bash
cd ~
git clone https://github.com/Accessiry/vulweb.git
cd vulweb
```

### 2. 运行安装脚本

```bash
chmod +x scripts/*.sh
./scripts/install.sh
```

### 3. 安装依赖

#### 后端依赖
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

#### 前端依赖
```bash
cd frontend
npm install
cd ..
```

### 4. 启动系统

```bash
./scripts/start.sh
```

### 5. 访问系统

在Windows浏览器中打开：
- 前端: http://localhost:3000
- 后端API: http://localhost:5000

### 6. 停止系统

```bash
./scripts/stop.sh
```

## 手动部署

### 后端部署

1. **进入后端目录**
```bash
cd backend
```

2. **创建虚拟环境**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **创建必要目录**
```bash
mkdir -p uploads/models uploads/datasets training_outputs
```

5. **配置环境变量（可选）**
```bash
cp .env.example .env
# 编辑 .env 文件
nano .env
```

6. **启动后端**
```bash
python run.py
```

后端将在 http://localhost:5000 运行

### 前端部署

1. **进入前端目录**
```bash
cd frontend
```

2. **安装依赖**
```bash
npm install
```

3. **启动开发服务器**
```bash
npm run dev
```

前端将在 http://localhost:3000 运行

### 生产环境构建

#### 前端构建
```bash
cd frontend
npm run build
```

构建产物在 `frontend/dist` 目录。

## 配置说明

### 配置文件位置

- 系统配置: `config/config.ini`
- 后端环境变量: `backend/.env`
- 前端环境变量: `frontend/.env`

### 主要配置项

#### 后端配置 (config/config.ini)

```ini
[backend]
host = 0.0.0.0
port = 5000
debug = false

[database]
type = sqlite
path = app.db

[upload]
max_file_size = 524288000  # 500MB

[ai]
provider = qwen
api_key = your-api-key-here
endpoint = https://dashscope.aliyuncs.com/api/v1
model = qwen-turbo
```

#### AI服务商配置

系统支持以下国内AI服务：

1. **通义千问 (Qwen)**
   - 官网: https://tongyi.aliyun.com/
   - API文档: https://help.aliyun.com/zh/dashscope/
   - 配置:
     ```ini
     provider = qwen
     endpoint = https://dashscope.aliyuncs.com/api/v1
     api_key = your-api-key
     model = qwen-turbo
     ```

2. **文心一言 (ERNIE)**
   - 官网: https://yiyan.baidu.com/
   - API文档: https://cloud.baidu.com/doc/WENXINWORKSHOP/
   - 配置:
     ```ini
     provider = ernie
     endpoint = https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop
     api_key = your-api-key
     model = ernie-bot-turbo
     ```

3. **智谱AI (ChatGLM)**
   - 官网: https://open.bigmodel.cn/
   - API文档: https://open.bigmodel.cn/dev/api
   - 配置:
     ```ini
     provider = chatglm
     endpoint = https://open.bigmodel.cn/api/paas/v4/
     api_key = your-api-key
     model = chatglm_turbo
     ```

## WSL特定配置

### 访问WSL文件系统

从Windows访问WSL文件：
```
\\wsl$\Ubuntu\home\username\vulweb
```

### WSL与Windows网络

WSL 2使用虚拟网络，在Windows中访问WSL服务使用 `localhost`。

### 性能优化

1. **将项目放在WSL文件系统中**
   不要将项目放在 `/mnt/c/`下，这会影响性能。

2. **配置WSL内存限制**
   创建 `%UserProfile%\.wslconfig`:
   ```ini
   [wsl2]
   memory=4GB
   processors=2
   ```

## 开机自动启动

### 方法1: Windows任务计划程序

1. 创建启动脚本 `start_vulweb.bat`:
```batch
@echo off
wsl -d Ubuntu -u username -- /home/username/vulweb/scripts/start.sh
```

2. 打开任务计划程序
3. 创建基本任务
4. 触发器: 登录时
5. 操作: 启动程序，选择 `start_vulweb.bat`

### 方法2: WSL启动项

在WSL中添加到 `~/.bashrc`:
```bash
# VulWeb自动启动
if [ ! -f /tmp/vulweb_started ]; then
    ~/vulweb/scripts/start.sh
    touch /tmp/vulweb_started
fi
```

## 日志管理

日志文件位置：
- 后端日志: `logs/backend.log`
- 前端日志: `logs/frontend.log`
- 应用日志: `logs/app.log`

查看日志：
```bash
# 实时查看后端日志
tail -f logs/backend.log

# 实时查看前端日志
tail -f logs/frontend.log
```

## 常见问题

### 1. 端口已被占用

**错误**: `Address already in use`

**解决**:
```bash
# 查找占用端口的进程
netstat -ano | findstr :5000
netstat -ano | findstr :3000

# 在WSL中停止进程
kill -9 <PID>
```

### 2. npm install失败

**错误**: `EACCES: permission denied`

**解决**:
```bash
# 清理npm缓存
npm cache clean --force

# 修复权限
sudo chown -R $USER:$USER ~/.npm

# 重新安装
npm install
```

### 3. Python虚拟环境问题

**错误**: `No module named 'xxx'`

**解决**:
```bash
# 确保激活虚拟环境
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

### 4. 无法访问localhost

**问题**: Windows浏览器无法访问WSL服务

**解决**:
```bash
# 在WSL中查看IP
ip addr show eth0

# 在Windows中使用WSL IP访问
# 例如: http://172.x.x.x:3000
```

### 5. WSL2网络问题

**问题**: WSL无法访问外网

**解决**:
```bash
# 重启WSL网络
wsl --shutdown
wsl

# 或在Windows PowerShell中
Get-Service LxssManager | Restart-Service
```

### 6. 磁盘空间不足

**解决**:
```bash
# 清理apt缓存
sudo apt-get clean

# 清理npm缓存
npm cache clean --force

# 清理Python缓存
find . -type d -name __pycache__ -exec rm -r {} +
```

## 维护命令

### 更新系统

```bash
cd ~/vulweb
git pull origin main
./scripts/stop.sh
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..
./scripts/start.sh
```

### 备份数据

```bash
# 备份数据库
cp backend/app.db backup/app_$(date +%Y%m%d).db

# 备份上传文件
tar -czf backup/uploads_$(date +%Y%m%d).tar.gz backend/uploads

# 备份训练输出
tar -czf backup/training_$(date +%Y%m%d).tar.gz backend/training_outputs
```

### 清理旧数据

```bash
# 清理30天前的训练输出
find backend/training_outputs -mtime +30 -delete

# 清理日志文件
find logs -name "*.log" -mtime +7 -delete
```

## 安全建议

1. **修改默认密钥**
   ```bash
   # 生成新的密钥
   python3 -c "import secrets; print(secrets.token_hex(32))"
   # 更新到 config/config.ini
   ```

2. **使用环境变量存储敏感信息**
   ```bash
   export SECRET_KEY='your-secret-key'
   export AI_API_KEY='your-api-key'
   ```

3. **定期更新依赖**
   ```bash
   pip list --outdated
   npm outdated
   ```

4. **配置防火墙**
   ```bash
   sudo ufw allow 5000/tcp
   sudo ufw allow 3000/tcp
   ```

## 性能调优

### Python优化

```bash
# 使用更快的WSGI服务器
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Node.js优化

```bash
# 生产构建
npm run build

# 使用静态服务器
npm install -g serve
serve -s dist -l 3000
```

## 支持与反馈

- GitHub Issues: https://github.com/Accessiry/vulweb/issues
- 文档: https://github.com/Accessiry/vulweb/wiki
- Email: support@vulweb.com

## 相关资源

- WSL文档: https://docs.microsoft.com/zh-cn/windows/wsl/
- Vue.js文档: https://cn.vuejs.org/
- Flask文档: https://flask.palletsprojects.com/
- Element Plus文档: https://element-plus.org/zh-CN/
