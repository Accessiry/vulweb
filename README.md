# VulWeb - 代码漏洞检测模型管理系统

一个完整的Web平台，用于代码漏洞检测机器学习模型的管理、训练和评估。系统提供直观的界面来管理模型、数据集和训练任务，支持实时监控和可视化，专为Windows WSL环境优化。

## 功能特性

### 🔧 模型管理
- 上传和注册机器学习模型
- 查看模型信息和性能指标
- 支持多种模型类型（漏洞检测、细粒度定位）
- 版本管理和追踪

### 📊 数据集管理
- 上传和存储数据集
- 自动格式验证（JSON, CSV, TXT, ZIP）
- 数据集统计信息和预处理
- 支持代码漏洞检测数据格式

### 🚀 训练与验证
- 创建和管理训练任务
- 实时训练进度监控
- 交互式指标可视化（ECharts）
- 训练历史和结果分析
- 一键启动训练

### 💬 AI对话智能体
- 智能问答助手
- 操作指导和帮助
- 系统状态查询
- 支持国内AI服务（通义千问、文心一言等）

### 🎨 用户界面
- 现代化响应式Web界面
- 直观的模块导航
- 实时数据更新
- 交互式图表和可视化
- 暗黑模式支持

### ⚙️ 系统设置
- AI API配置
- 系统参数调整
- 数据管理工具

## 技术栈

### 后端
- **框架**: Flask 3.0
- **数据库**: SQLAlchemy + SQLite（可切换到PostgreSQL）
- **API**: RESTful设计，支持CORS
- **文件处理**: Werkzeug

### 前端
- **框架**: Vue.js 3.3
- **UI组件**: Element Plus 2.4（国内可访问）
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **图表**: ECharts 5.4（百度出品，国内友好）
- **构建工具**: Vite 5

### 部署环境
- **目标平台**: Windows WSL (Ubuntu)
- **无需Docker**: 直接部署，易于维护
- **一键脚本**: 自动化安装和启动

## 项目结构

```
vulweb/
├── backend/                          # Flask后端
│   ├── app/                          # 主应用
│   │   ├── api/                      # API端点
│   │   │   ├── models.py            # 模型管理API
│   │   │   ├── datasets.py          # 数据集管理API
│   │   │   ├── training.py          # 训练任务API
│   │   │   └── chat.py              # AI对话API
│   │   ├── models/                   # 数据库模型
│   │   ├── services/                 # 业务逻辑
│   │   └── utils/                    # 工具函数
│   ├── config/                       # 配置文件
│   ├── requirements.txt              # Python依赖
│   └── run.py                        # 入口文件
├── frontend/                         # Vue.js前端
│   ├── src/
│   │   ├── views/                    # 页面组件
│   │   │   ├── Dashboard.vue        # 首页Dashboard
│   │   │   ├── Models.vue           # 模型管理
│   │   │   ├── Datasets.vue         # 数据集管理
│   │   │   ├── Training.vue         # 训练任务
│   │   │   ├── Results.vue          # 结果展示
│   │   │   ├── Chat.vue             # AI对话
│   │   │   └── Settings.vue         # 系统设置
│   │   ├── router/                   # 路由配置
│   │   ├── api/                      # API服务
│   │   └── App.vue                   # 主应用
│   ├── package.json                  # Node.js依赖
│   └── vite.config.js                # Vite配置
├── scripts/                          # 部署脚本
│   ├── install.sh                    # 环境安装脚本
│   ├── start.sh                      # 启动脚本
│   └── stop.sh                       # 停止脚本
├── config/                           # 系统配置
│   └── config.ini                    # 配置文件
├── docs/                             # 文档
│   ├── WSL_DEPLOYMENT.md            # WSL部署指南
│   └── USER_GUIDE.md                # 用户手册
├── models/                           # 模型存储目录
├── datasets/                         # 数据集存储目录
└── logs/                             # 日志目录
```

## 快速开始（WSL环境）

### 前置要求
- Windows 10/11 with WSL 2
- Python 3.10+
- Node.js 18+
- 至少4GB RAM

### 一键部署

1. **安装WSL**（如已安装跳过）
```powershell
# 在Windows PowerShell（管理员）中运行
wsl --install
```

2. **启动WSL并克隆项目**
```bash
wsl
cd ~
git clone https://github.com/Accessiry/vulweb.git
cd vulweb
```

3. **运行安装脚本**
```bash
./scripts/install.sh
```

4. **安装依赖**
```bash
# 后端依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 前端依赖
cd frontend
npm install
cd ..
```

5. **启动系统**
```bash
./scripts/start.sh
```

6. **访问系统**
在Windows浏览器中打开：
- **前端**: http://localhost:3000
- **后端API**: http://localhost:5000

7. **停止系统**
```bash
./scripts/stop.sh
```

### 手动部署

详细的手动部署步骤请参考 [WSL部署指南](docs/WSL_DEPLOYMENT.md)。

## 使用指南

### 1. 管理模型

**添加新模型:**
1. 进入"模型管理"页面
2. 点击"上传模型"按钮
3. 填写模型信息：
   - 名称（必填）
   - 描述
   - 版本
   - 模型类型
   - 上传模型文件（.pkl, .pt, .pth, .h5, .onnx）
4. 点击"上传"

**查看模型:**
- 所有模型以卡片形式展示
- 每个卡片显示名称、描述、类型、版本和准确率

**删除模型:**
- 点击模型卡片上的删除图标

### 2. 管理数据集

**上传数据集:**
1. 进入"数据集管理"页面
2. 点击"上传数据集"按钮
3. 填写数据集信息：
   - 名称（必填）
   - 描述
   - 上传数据集文件（.json, .csv, .txt, .zip）
4. 点击"上传"

**查看数据集统计:**
- 每个数据集卡片显示：
  - 格式
  - 文件大小
  - 样本数量
  - 漏洞样本数/安全样本数
  - 预处理状态

**删除数据集:**
- 点击数据集卡片上的删除图标

### 3. 训练模型

**开始训练:**
1. 进入"训练任务"页面
2. 点击"创建训练任务"按钮
3. 配置训练任务：
   - 任务名称
   - 选择模型
   - 选择数据集
   - 设置训练轮次（epochs）
4. 点击"创建并开始训练"

**监控训练:**
- 查看实时训练进度
- 交互式图表显示：
  - Loss随时间变化
  - Accuracy随时间变化
  - 训练集 vs 验证集指标
- 当前指标显示：
  - Loss
  - Accuracy
  - Validation Loss
  - Validation Accuracy

**管理任务:**
- 停止运行中的任务
- 删除已完成的任务
- 查看训练历史

### 4. AI对话

**使用AI助手:**
1. 进入"AI对话"页面
2. 在输入框中输入问题
3. 查看AI回复
4. 使用快捷问题快速提问

**配置AI服务:**
1. 进入"系统设置"
2. 配置AI API：
   - 选择服务商（通义千问、文心一言等）
   - 输入API Key
   - 设置Endpoint和模型
3. 测试连接
4. 保存配置

### 5. 查看结果

**查看训练结果:**
1. 进入"结果展示"页面
2. 浏览已完成的训练任务
3. 点击"查看详情"查看：
   - 训练配置
   - 最终性能指标
   - 完整训练曲线
   - 训练时长

## API文档

### 模型API

```
GET    /api/models          - 获取所有模型
GET    /api/models/:id      - 获取指定模型
POST   /api/models          - 创建新模型
PUT    /api/models/:id      - 更新模型
DELETE /api/models/:id      - 删除模型
```

### 数据集API

```
GET    /api/datasets             - 获取所有数据集
GET    /api/datasets/:id         - 获取指定数据集
POST   /api/datasets             - 创建新数据集
PUT    /api/datasets/:id         - 更新数据集
DELETE /api/datasets/:id         - 删除数据集
GET    /api/datasets/:id/stats   - 获取数据集统计
```

### 训练API

```
GET    /api/training/tasks                - 获取所有训练任务
GET    /api/training/tasks/:id            - 获取指定任务
POST   /api/training/tasks                - 创建新任务
POST   /api/training/tasks/:id/stop       - 停止任务
GET    /api/training/tasks/:id/metrics    - 获取任务指标
DELETE /api/training/tasks/:id            - 删除任务
```

### AI对话API

```
POST   /api/chat/message      - 发送消息
GET    /api/chat/history      - 获取对话历史
DELETE /api/chat/history      - 清空对话历史
```

## 集成训练代码

系统提供标准化接口用于集成自定义训练代码。

### 训练服务集成

编辑 `backend/app/services/training_service.py`:

```python
def start_training_task(task_id, config):
    """在此集成您的训练代码"""
    task = TrainingTask.query.get(task_id)
    
    # 导入您的训练模块
    from your_module import train_model
    
    # 调用训练函数
    train_model(
        model_path=task.model.file_path,
        dataset_path=task.dataset.file_path,
        epochs=config.get('epochs'),
        task_id=task_id
    )
```

### 报告训练进度

在训练过程中向API报告指标：

```python
import requests

def report_progress(task_id, epoch, metrics):
    requests.post(
        f'http://localhost:5000/api/training/tasks/{task_id}/metrics',
        json={
            'epoch': epoch,
            'loss': metrics['loss'],
            'accuracy': metrics['accuracy'],
            'validation_loss': metrics['val_loss'],
            'validation_accuracy': metrics['val_accuracy'],
            'learning_rate': metrics['lr']
        }
    )
```

## 配置

### 后端配置

编辑 `config/config.ini`:

```ini
[backend]
host = 0.0.0.0
port = 5000
secret_key = your-secret-key-here

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

### 前端配置

在frontend目录创建 `.env` 文件：

```
VITE_API_URL=http://localhost:5000/api
```

## 开发

### 运行测试

后端：
```bash
cd backend
pytest
```

前端：
```bash
cd frontend
npm test
```

### 代码风格

- 后端遵循Flask最佳实践
- 前端遵循Vue.js 3 Composition API风格
- 使用Element Plus组件规范

## 故障排除

### 常见问题

**后端无法启动:**
- 检查Python版本（需要3.10+）
- 确保所有依赖已安装
- 验证数据库可访问

**前端无法启动:**
- 检查Node版本（需要18+）
- 清除npm缓存：`npm cache clean --force`
- 删除node_modules并重新安装

**训练任务无法启动:**
- 检查模型和数据集文件是否存在
- 验证文件路径正确
- 查看后端日志

**端口被占用:**
```bash
# 查找占用端口的进程
netstat -ano | findstr :5000
netstat -ano | findstr :3000

# 停止进程
kill -9 <PID>
```

详细故障排除请参考 [WSL部署指南](docs/WSL_DEPLOYMENT.md)。

## 文档

- [WSL部署指南](docs/WSL_DEPLOYMENT.md) - 完整的WSL环境部署说明
- [用户手册](docs/USER_GUIDE.md) - 详细的功能使用指南
- [项目结构](PROJECT_STRUCTURE.md) - 代码结构说明
- [快速开始](QUICKSTART.md) - 快速入门指南

## 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)。

## 许可证

本项目采用MIT许可证。

## 支持

如有问题或建议：
- 创建GitHub Issue
- 发送邮件至：support@vulweb.com
- 查看文档和Wiki

## 致谢

使用以下优秀的开源技术构建：
- Vue.js 3 - 渐进式JavaScript框架
- Element Plus - Vue 3 UI组件库
- Flask - Python Web框架
- ECharts - 数据可视化库
- SQLAlchemy - Python ORM

## 路线图

- [x] 基础模型管理
- [x] 数据集管理
- [x] 训练任务系统
- [x] AI对话功能
- [x] WSL部署支持
- [ ] PostgreSQL支持
- [ ] 用户认证和授权
- [ ] 高级模型分析
- [ ] 分布式训练支持
- [ ] 模型版本对比
- [ ] Kubernetes部署支持