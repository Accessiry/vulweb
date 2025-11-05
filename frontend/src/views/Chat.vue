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
    // Send message to backend RAG service
    const response = await chatAPI.sendMessage({ content: question })
    
    const aiMessage = {
      role: 'assistant',
      content: response.content,
      timestamp: response.timestamp
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
  let formatted = content
    // Bold text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Code blocks (inline)
    .replace(/`(.+?)`/g, '<code>$1</code>')
    // Links
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>')
    // Line breaks
    .replace(/\n/g, '<br/>')
    // Lists (simple handling)
    .replace(/^- (.+?)(<br\/>|$)/gm, '• $1$2')
    .replace(/^(\d+)\. (.+?)(<br\/>|$)/gm, '$1. $2$3')
  
  return formatted
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

.message-text code {
  background-color: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.message.user .message-text code {
  background-color: rgba(255, 255, 255, 0.2);
}

.message-text a {
  color: #409eff;
  text-decoration: none;
}

.message-text a:hover {
  text-decoration: underline;
}

.message.user .message-text a {
  color: #fff;
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
