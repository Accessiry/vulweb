<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">AI对话智能体</h2>
      <el-button @click="clearChat" :icon="Delete">清空对话</el-button>
    </div>

    <el-card class="chat-container">
      <!-- 消息列表 -->
      <div class="messages-container" ref="messagesRef">
        <div v-if="messages.length === 0" class="empty-chat">
          <el-icon :size="60" color="#909399"><ChatDotRound /></el-icon>
          <p>开始与AI对话，可以询问关于模型、数据集和训练的问题</p>
        </div>
        
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.role]"
        >
          <div class="message-avatar">
            <el-avatar :size="40" :icon="message.role === 'user' ? User : Robot" />
          </div>
          <div class="message-content">
            <div class="message-header">
              <span class="message-role">
                {{ message.role === 'user' ? '用户' : 'AI助手' }}
              </span>
              <span class="message-time">{{ formatTime(message.timestamp) }}</span>
            </div>
            <div class="message-text" v-html="formatMessage(message.content)"></div>
          </div>
        </div>

        <!-- 加载中 -->
        <div v-if="loading" class="message assistant">
          <div class="message-avatar">
            <el-avatar :size="40" :icon="Robot" />
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入框 -->
      <div class="input-container">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="输入您的问题，例如：如何上传模型？训练任务的状态是什么？"
          @keydown.enter.prevent="handleEnter"
        />
        <el-button
          type="primary"
          :disabled="!inputMessage.trim() || loading"
          @click="sendMessage"
          :loading="loading"
        >
          <el-icon><Promotion /></el-icon>
          发送
        </el-button>
      </div>

      <!-- 快捷问题 -->
      <div class="quick-questions">
        <span style="margin-right: 10px; color: #909399;">快捷问题：</span>
        <el-tag
          v-for="(question, index) in quickQuestions"
          :key="index"
          style="margin-right: 10px; cursor: pointer;"
          @click="askQuestion(question)"
        >
          {{ question }}
        </el-tag>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { chatAPI, modelsAPI, datasetsAPI, trainingAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, User, Robot, Promotion, ChatDotRound } from '@element-plus/icons-vue'

const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)
const messagesRef = ref(null)

const quickQuestions = [
  '如何上传模型？',
  '训练任务的状态是什么？',
  '有多少个数据集？',
  '如何创建训练任务？'
]

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = {
    role: 'user',
    content: inputMessage.value,
    timestamp: new Date().toISOString()
  }
  
  messages.value.push(userMessage)
  const question = inputMessage.value
  inputMessage.value = ''
  
  await nextTick()
  scrollToBottom()
  
  loading.value = true
  
  try {
    // Get context data
    const [models, datasets, tasks] = await Promise.all([
      modelsAPI.getAll(),
      datasetsAPI.getAll(),
      trainingAPI.getTasks()
    ])
    
    // Generate AI response based on question
    const response = await generateResponse(question, { models, datasets, tasks })
    
    const aiMessage = {
      role: 'assistant',
      content: response,
      timestamp: new Date().toISOString()
    }
    
    messages.value.push(aiMessage)
    
    await nextTick()
    scrollToBottom()
  } catch (error) {
    ElMessage.error('发送消息失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const generateResponse = async (question, context) => {
  const q = question.toLowerCase()
  
  // Model related questions
  if (q.includes('模型') || q.includes('model')) {
    if (q.includes('上传') || q.includes('添加')) {
      return `要上传模型，请按照以下步骤操作：

1. 点击左侧菜单的"模型管理"
2. 点击页面右上角的"上传模型"按钮
3. 填写模型信息：
   - 模型名称（必填）
   - 描述（可选）
   - 版本号（默认1.0.0）
   - 模型类型（选择漏洞检测或细粒度定位）
4. 选择模型文件（支持.pkl, .pt, .pth, .h5, .onnx格式）
5. 点击"上传"按钮

当前系统中有 <strong>${context.models.length}</strong> 个模型。`
    }
    
    if (q.includes('多少') || q.includes('数量')) {
      const modelList = context.models.map((m, i) => `${i + 1}. ${m.name} (${m.model_type || '未指定类型'})`).join('\n')
      return `当前系统中共有 <strong>${context.models.length}</strong> 个模型：

${modelList || '暂无模型'}

您可以在"模型管理"页面查看详细信息。`
    }
  }
  
  // Dataset related questions
  if (q.includes('数据集') || q.includes('dataset')) {
    if (q.includes('上传') || q.includes('添加')) {
      return `要上传数据集，请按照以下步骤操作：

1. 点击左侧菜单的"数据集管理"
2. 点击页面右上角的"上传数据集"按钮
3. 填写数据集信息：
   - 数据集名称（必填）
   - 描述（可选）
4. 选择数据集文件（支持.json, .csv, .txt, .zip格式）
5. 点击"上传"按钮

系统会自动分析数据集内容，提取样本数量和漏洞/安全样本的分布。

当前系统中有 <strong>${context.datasets.length}</strong> 个数据集。`
    }
    
    if (q.includes('多少') || q.includes('数量')) {
      const datasetList = context.datasets.map((d, i) => 
        `${i + 1}. ${d.name} (${d.num_samples || 0}个样本)`
      ).join('\n')
      return `当前系统中共有 <strong>${context.datasets.length}</strong> 个数据集：

${datasetList || '暂无数据集'}

您可以在"数据集管理"页面查看详细统计信息。`
    }
  }
  
  // Training related questions
  if (q.includes('训练') || q.includes('training') || q.includes('任务')) {
    if (q.includes('创建') || q.includes('开始') || q.includes('如何')) {
      return `要创建训练任务，请按照以下步骤操作：

1. 确保已上传模型和数据集
2. 点击左侧菜单的"训练任务"
3. 点击页面右上角的"创建训练任务"按钮
4. 填写训练配置：
   - 任务名称
   - 选择模型
   - 选择数据集
   - 设置训练轮次（epochs）
5. 点击"创建并开始训练"按钮

系统会自动开始训练，您可以实时查看训练进度和指标。

当前有 <strong>${context.tasks.filter(t => t.status === 'running').length}</strong> 个任务正在运行，
<strong>${context.tasks.filter(t => t.status === 'completed').length}</strong> 个任务已完成。`
    }
    
    if (q.includes('状态') || q.includes('进度')) {
      const runningTasks = context.tasks.filter(t => t.status === 'running')
      const completedTasks = context.tasks.filter(t => t.status === 'completed')
      const pendingTasks = context.tasks.filter(t => t.status === 'pending')
      const failedTasks = context.tasks.filter(t => t.status === 'failed')
      
      return `训练任务状态统计：

- 🔄 运行中：<strong>${runningTasks.length}</strong> 个
- ✅ 已完成：<strong>${completedTasks.length}</strong> 个
- ⏳ 等待中：<strong>${pendingTasks.length}</strong> 个
- ❌ 失败：<strong>${failedTasks.length}</strong> 个

总计：<strong>${context.tasks.length}</strong> 个训练任务

您可以在"训练任务"页面查看详细信息和实时指标。`
    }
  }
  
  // System related questions
  if (q.includes('系统') || q.includes('功能') || q.includes('帮助')) {
    return `VulWeb 代码漏洞检测模型管理系统主要功能：

📦 <strong>模型管理</strong>
- 上传和管理机器学习模型
- 查看模型性能指标
- 支持多种模型格式

📊 <strong>数据集管理</strong>
- 上传和管理训练数据集
- 自动分析数据集统计信息
- 支持多种数据格式

🚀 <strong>训练任务</strong>
- 创建和管理训练任务
- 实时监控训练进度
- 可视化训练指标

📈 <strong>结果展示</strong>
- 查看训练历史和结果
- 交互式图表可视化
- 性能指标分析

💬 <strong>AI对话</strong>
- 智能问答助手
- 快速操作指导

⚙️ <strong>系统设置</strong>
- AI API配置
- 系统参数设置

如需帮助，可以询问具体功能的使用方法！`
  }
  
  // Default response
  return `抱歉，我不太理解您的问题。您可以尝试询问：

- 如何上传模型？
- 如何创建训练任务？
- 当前有多少个数据集？
- 训练任务的状态是什么？
- 系统有哪些功能？

或者点击下方的快捷问题开始对话。`
}

const askQuestion = (question) => {
  inputMessage.value = question
  sendMessage()
}

const handleEnter = (e) => {
  if (!e.shiftKey) {
    sendMessage()
  }
}

const clearChat = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有对话记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    messages.value = []
    ElMessage.success('对话已清空')
  } catch (error) {
    // User cancelled
  }
}

const scrollToBottom = () => {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatMessage = (content) => {
  // Convert markdown-like formatting to HTML
  return content
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br/>')
}

onMounted(() => {
  // Add welcome message
  messages.value.push({
    role: 'assistant',
    content: '您好！我是VulWeb AI助手，很高兴为您服务。\n\n我可以帮您：\n- 了解系统功能\n- 指导操作流程\n- 查询系统状态\n- 解答使用问题\n\n请随时向我提问！',
    timestamp: new Date().toISOString()
  })
})
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 180px);
  display: flex;
  flex-direction: column;
}

.chat-container :deep(.el-card__body) {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7fa;
}

.empty-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

.empty-chat p {
  margin-top: 20px;
  font-size: 14px;
}

.message {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.message.user .message-avatar {
  margin-left: 12px;
}

.message.assistant .message-avatar {
  margin-right: 12px;
}

.message-content {
  max-width: 70%;
  background: white;
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message.user .message-content {
  background: #409eff;
  color: white;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 12px;
  opacity: 0.8;
}

.message-role {
  font-weight: 600;
}

.message-text {
  line-height: 1.6;
  word-wrap: break-word;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: #409eff;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.input-container {
  display: flex;
  gap: 12px;
  padding: 20px;
  background: white;
  border-top: 1px solid #e4e7ed;
}

.input-container .el-input {
  flex: 1;
}

.quick-questions {
  padding: 12px 20px;
  background: white;
  border-top: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
</style>
