# Changelog

All notable changes to the VulWeb project are documented in this file.

## [2.0.0] - 2024-11-05

### 🎉 Major Refactor: Vue.js 3 + Element Plus Migration

This release represents a complete rewrite of the frontend using Vue.js 3 and Element Plus, along with significant enhancements for WSL deployment and AI capabilities.

### Added

#### Frontend (Vue.js 3 + Element Plus)
- **完整的Vue.js 3前端重构**
  - 使用Vue 3 Composition API
  - Element Plus UI组件库（国内可访问）
  - Vite构建工具（快速HMR）
  - Pinia状态管理
  
- **七个核心页面**
  - `Dashboard.vue` - 首页仪表盘，显示系统统计和快速操作
  - `Models.vue` - 模型管理页面，支持上传、查看、删除模型
  - `Datasets.vue` - 数据集管理页面，支持上传、统计、删除数据集
  - `Training.vue` - 训练任务页面，创建任务、实时监控、ECharts可视化
  - `Results.vue` - 结果展示页面，查看训练历史和详细指标
  - `Chat.vue` - AI对话页面，智能助手功能
  - `Settings.vue` - 系统设置页面，AI配置和系统参数
  
- **UI功能增强**
  - 响应式布局设计
  - 暗黑模式支持
  - 中文界面和i18n支持
  - 交互式图表（ECharts）
  - 优雅的动画过渡
  - 表单验证
  - 文件上传进度
  
#### Backend (Flask)
- **AI对话API (`/api/chat`)**
  - `POST /api/chat/message` - 发送消息获取AI回复
  - `GET /api/chat/history` - 获取对话历史
  - `DELETE /api/chat/history` - 清空对话历史
  - 支持国内AI服务集成（通义千问、文心一言、智谱AI等）
  
#### WSL部署支持
- **一键部署脚本**
  - `scripts/install.sh` - 自动安装环境依赖
  - `scripts/start.sh` - 一键启动前后端服务
  - `scripts/stop.sh` - 优雅停止所有服务
  
- **配置文件**
  - `config/config.ini` - 统一的系统配置文件
  - 支持AI API配置
  - 支持数据库配置
  - 支持上传和训练参数配置
  
#### 文档
- **WSL部署指南** (`docs/WSL_DEPLOYMENT.md`)
  - 完整的WSL安装步骤
  - 环境准备说明
  - 快速部署指南
  - 手动部署步骤
  - AI服务商配置详解
  - 常见问题解答
  - 性能优化建议
  
- **用户手册** (`docs/USER_GUIDE.md`)
  - 系统概述
  - 详细功能说明
  - 操作步骤指导
  - 最佳实践
  - 故障排除
  - 术语表
  
- **测试指南** (`docs/TESTING_GUIDE.md`)
  - 20+测试用例
  - 功能测试步骤
  - 性能测试方法
  - 错误处理测试
  - 浏览器兼容性测试
  - 测试报告模板
  
- **目录README文件**
  - `models/README.md` - 模型存储说明
  - `datasets/README.md` - 数据集格式说明
  - `logs/README.md` - 日志管理说明
  
#### 示例数据
- **样本数据集** (`datasets/sample_dataset.json`)
  - 16个代码样本（8个漏洞 + 8个安全）
  - 涵盖7种常见漏洞类型：
    - SQL注入
    - 命令注入
    - 代码注入
    - 不安全的反序列化
    - 路径遍历
    - 硬编码凭证
    - 弱随机数
    - XSS
  - JSON格式，可直接使用
  
### Changed

#### Frontend Migration
- **从React迁移到Vue.js 3**
  - 移除React、React Router、Recharts依赖
  - 添加Vue 3、Vue Router 4、Pinia依赖
  - 使用Element Plus替代自定义UI组件
  - 使用ECharts替代Recharts
  - 使用Vite替代Create React App
  
- **构建系统**
  - `package.json` - 更新为Vue 3生态系统
  - `vite.config.js` - Vite配置文件（替代CRA）
  - 移除Docker配置（前端）
  
#### Backend Updates
- **集成AI对话模块**
  - 注册chat_bp蓝图
  - 添加模拟AI响应生成器
  - 支持多AI服务商配置
  
#### 文档更新
- **README.md** 
  - 更新技术栈说明（Vue.js 3 + Element Plus）
  - 添加WSL部署说明
  - 更新快速开始指南
  - 添加中文文档
  - 移除Docker部署说明
  
- **.gitignore**
  - 添加Vue/Vite特定忽略规则
  - 添加日志文件忽略规则
  - 添加备份目录忽略规则

### Removed
- **React前端**
  - 移除所有React组件
  - 移除React配置文件
  - 移除Nginx配置（前端）
  - 移除Dockerfile（前端）
  
- **Docker配置**
  - 前端不再使用Docker部署
  - 专注于WSL原生部署

### Technical Details

#### 依赖版本
**Frontend:**
- Vue.js: 3.3.8
- Vue Router: 4.2.5
- Pinia: 2.1.7
- Element Plus: 2.4.4
- ECharts: 5.4.3
- Axios: 1.6.2
- Vite: 5.0.4

**Backend:**
- Flask: 3.0.0
- SQLAlchemy: 2.0.23
- Flask-CORS: 4.0.0
- Python: 3.10+

#### 架构变化
```
之前: React + CRA + Recharts + Docker
现在: Vue 3 + Vite + ECharts + WSL Native
```

#### API兼容性
- 所有现有API端点保持兼容
- 新增AI对话API端点
- 响应格式保持不变

### Migration Guide

#### 从v1.0到v2.0

1. **备份数据**
   ```bash
   cp backend/app.db backup/
   tar -czf backup/uploads.tar.gz backend/uploads/
   ```

2. **更新代码**
   ```bash
   git pull origin main
   ```

3. **重新安装依赖**
   ```bash
   # 前端
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   
   # 后端
   cd ../backend
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **启动系统**
   ```bash
   cd ..
   ./scripts/start.sh
   ```

### Breaking Changes

⚠️ **重要**: 此版本包含破坏性更改

1. **前端完全重写**
   - 不兼容React代码
   - 需要重新安装依赖
   - API调用方式相同，但前端实现完全不同

2. **部署方式变更**
   - 不再使用Docker Compose
   - 改用WSL原生部署
   - 需要使用新的启动脚本

3. **配置文件位置**
   - 新增`config/config.ini`
   - 前端环境变量使用`.env`而非`REACT_APP_*`

### Known Issues

- AI对话功能使用模拟响应，需要配置实际AI API
- 训练服务使用模拟数据，需要集成实际训练代码
- 不支持分布式训练（计划中）

### Performance Improvements

- Vite提供更快的开发服务器启动
- Vue 3的响应式系统性能更好
- Element Plus组件按需加载
- ECharts图表渲染优化

### Security

- 添加表单验证
- 文件上传类型检查
- API密钥安全存储（localStorage）
- CORS配置保持

### Contributors

- @Accessiry - 项目维护者

### Notes

此版本代表项目向现代化、国内友好的技术栈的重大迁移。选择Vue.js 3和Element Plus是为了更好地服务国内用户，提供更快的访问速度和更丰富的中文文档。

WSL部署方式的选择使得Windows用户能够更轻松地在本地开发和部署系统，无需复杂的Docker配置。

### Roadmap for v2.1

- [ ] 集成真实AI API（通义千问、文心一言）
- [ ] 添加用户认证系统
- [ ] PostgreSQL支持
- [ ] 模型版本对比功能
- [ ] 批量训练任务
- [ ] 导出训练报告
- [ ] 更多图表类型
- [ ] 移动端适配

---

## [1.0.0] - 2024-11 (Previous)

### Initial Release
- React前端实现
- Flask后端API
- 基础模型管理
- 数据集管理
- 训练任务系统
- Docker部署支持
