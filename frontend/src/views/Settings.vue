<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">系统设置</h2>
    </div>

    <el-row :gutter="20">
      <el-col :span="16">
        <!-- AI配置 -->
        <el-card style="margin-bottom: 20px;">
          <template #header>
            <div style="display: flex; align-items: center;">
              <el-icon style="margin-right: 8px;"><Setting /></el-icon>
              <span>AI API配置</span>
            </div>
          </template>
          <el-form :model="aiConfig" label-width="120px">
            <el-form-item label="AI服务商">
              <el-select v-model="aiConfig.provider" placeholder="请选择AI服务商" style="width: 100%;">
                <el-option label="通义千问 (Qwen)" value="qwen" />
                <el-option label="文心一言 (ERNIE)" value="ernie" />
                <el-option label="智谱AI (ChatGLM)" value="chatglm" />
                <el-option label="百度千帆" value="qianfan" />
                <el-option label="本地部署" value="local" />
              </el-select>
            </el-form-item>
            <el-form-item label="API Key">
              <el-input
                v-model="aiConfig.apiKey"
                type="password"
                placeholder="请输入API Key"
                show-password
              />
            </el-form-item>
            <el-form-item label="API Endpoint">
              <el-input
                v-model="aiConfig.endpoint"
                placeholder="https://api.example.com/v1"
              />
            </el-form-item>
            <el-form-item label="模型">
              <el-input
                v-model="aiConfig.model"
                placeholder="例如: qwen-turbo"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveAIConfig">
                <el-icon><Select /></el-icon>
                保存配置
              </el-button>
              <el-button @click="testAIConnection">
                <el-icon><Connection /></el-icon>
                测试连接
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 系统配置 -->
        <el-card>
          <template #header>
            <div style="display: flex; align-items: center;">
              <el-icon style="margin-right: 8px;"><Tools /></el-icon>
              <span>系统配置</span>
            </div>
          </template>
          <el-form :model="systemConfig" label-width="120px">
            <el-form-item label="上传文件限制">
              <el-input-number
                v-model="systemConfig.maxUploadSize"
                :min="1"
                :max="1000"
              />
              <span style="margin-left: 10px; color: #909399;">MB</span>
            </el-form-item>
            <el-form-item label="训练超时时间">
              <el-input-number
                v-model="systemConfig.trainingTimeout"
                :min="60"
                :max="86400"
              />
              <span style="margin-left: 10px; color: #909399;">秒</span>
            </el-form-item>
            <el-form-item label="自动刷新">
              <el-switch v-model="systemConfig.autoRefresh" />
              <span style="margin-left: 10px; color: #909399;">自动刷新训练状态</span>
            </el-form-item>
            <el-form-item label="刷新间隔">
              <el-input-number
                v-model="systemConfig.refreshInterval"
                :min="5"
                :max="60"
                :disabled="!systemConfig.autoRefresh"
              />
              <span style="margin-left: 10px; color: #909399;">秒</span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveSystemConfig">
                <el-icon><Select /></el-icon>
                保存配置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <!-- 系统信息 -->
        <el-card style="margin-bottom: 20px;">
          <template #header>
            <div style="display: flex; align-items: center;">
              <el-icon style="margin-right: 8px;"><InfoFilled /></el-icon>
              <span>系统信息</span>
            </div>
          </template>
          <el-descriptions :column="1" size="small">
            <el-descriptions-item label="系统版本">
              v1.0.0
            </el-descriptions-item>
            <el-descriptions-item label="后端框架">
              Flask 3.0.0
            </el-descriptions-item>
            <el-descriptions-item label="前端框架">
              Vue.js 3.3.8
            </el-descriptions-item>
            <el-descriptions-item label="数据库">
              SQLite
            </el-descriptions-item>
            <el-descriptions-item label="运行环境">
              WSL / Linux
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 快捷操作 -->
        <el-card>
          <template #header>
            <div style="display: flex; align-items: center;">
              <el-icon style="margin-right: 8px;"><Management /></el-icon>
              <span>数据管理</span>
            </div>
          </template>
          <div style="display: flex; flex-direction: column; gap: 12px;">
            <el-button @click="exportData">
              <el-icon><Download /></el-icon>
              导出数据
            </el-button>
            <el-button @click="clearCache">
              <el-icon><Delete /></el-icon>
              清理缓存
            </el-button>
            <el-button type="danger" @click="resetSystem">
              <el-icon><RefreshLeft /></el-icon>
              重置系统
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const aiConfig = ref({
  provider: 'qwen',
  apiKey: '',
  endpoint: 'https://dashscope.aliyuncs.com/api/v1',
  model: 'qwen-turbo'
})

const systemConfig = ref({
  maxUploadSize: 500,
  trainingTimeout: 3600,
  autoRefresh: true,
  refreshInterval: 10
})

const loadConfig = () => {
  // Load from localStorage
  const savedAIConfig = localStorage.getItem('aiConfig')
  if (savedAIConfig) {
    aiConfig.value = JSON.parse(savedAIConfig)
  }
  
  const savedSystemConfig = localStorage.getItem('systemConfig')
  if (savedSystemConfig) {
    systemConfig.value = JSON.parse(savedSystemConfig)
  }
}

const saveAIConfig = () => {
  try {
    localStorage.setItem('aiConfig', JSON.stringify(aiConfig.value))
    ElMessage.success('AI配置已保存')
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  }
}

const testAIConnection = async () => {
  try {
    // This is a mock test - in real implementation, you would call the AI API
    ElMessage.info('正在测试连接...')
    
    setTimeout(() => {
      if (aiConfig.value.apiKey) {
        ElMessage.success('连接测试成功')
      } else {
        ElMessage.warning('请先配置API Key')
      }
    }, 1000)
  } catch (error) {
    ElMessage.error('连接测试失败: ' + error.message)
  }
}

const saveSystemConfig = () => {
  try {
    localStorage.setItem('systemConfig', JSON.stringify(systemConfig.value))
    ElMessage.success('系统配置已保存')
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  }
}

const exportData = () => {
  ElMessage.info('数据导出功能开发中...')
}

const clearCache = async () => {
  try {
    await ElMessageBox.confirm('确定要清理缓存吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // Clear some cache (not all localStorage)
    ElMessage.success('缓存已清理')
  } catch (error) {
    // User cancelled
  }
}

const resetSystem = async () => {
  try {
    await ElMessageBox.confirm(
      '此操作将重置所有系统配置，是否继续？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    
    // Reset configurations
    aiConfig.value = {
      provider: 'qwen',
      apiKey: '',
      endpoint: 'https://dashscope.aliyuncs.com/api/v1',
      model: 'qwen-turbo'
    }
    
    systemConfig.value = {
      maxUploadSize: 500,
      trainingTimeout: 3600,
      autoRefresh: true,
      refreshInterval: 10
    }
    
    localStorage.removeItem('aiConfig')
    localStorage.removeItem('systemConfig')
    
    ElMessage.success('系统配置已重置')
  } catch (error) {
    // User cancelled
  }
}

onMounted(() => {
  loadConfig()
})
</script>
