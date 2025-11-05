<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">首页Dashboard</h2>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-card class="stat-card primary" shadow="hover">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">模型总数</div>
              <div style="font-size: 32px; font-weight: bold;">{{ stats.totalModels }}</div>
            </div>
            <el-icon :size="50" style="opacity: 0.3;"><Box /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card success" shadow="hover">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">数据集数量</div>
              <div style="font-size: 32px; font-weight: bold;">{{ stats.totalDatasets }}</div>
            </div>
            <el-icon :size="50" style="opacity: 0.3;"><Folder /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card warning" shadow="hover">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">训练任务</div>
              <div style="font-size: 32px; font-weight: bold;">{{ stats.totalTasks }}</div>
            </div>
            <el-icon :size="50" style="opacity: 0.3;"><Connection /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card danger" shadow="hover">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">运行中</div>
              <div style="font-size: 32px; font-weight: bold;">{{ stats.runningTasks }}</div>
            </div>
            <el-icon :size="50" style="opacity: 0.3;"><Timer /></el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快速操作 -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div style="display: flex; align-items: center;">
              <el-icon style="margin-right: 8px;"><Lightning /></el-icon>
              <span>快速操作</span>
            </div>
          </template>
          <div style="display: flex; gap: 20px;">
            <el-button type="primary" @click="goTo('/models')">
              <el-icon><Upload /></el-icon>
              上传模型
            </el-button>
            <el-button type="success" @click="goTo('/datasets')">
              <el-icon><FolderAdd /></el-icon>
              上传数据集
            </el-button>
            <el-button type="warning" @click="goTo('/training')">
              <el-icon><VideoPlay /></el-icon>
              开始训练
            </el-button>
            <el-button type="info" @click="goTo('/chat')">
              <el-icon><ChatDotRound /></el-icon>
              AI对话
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近活动 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <div>
                <el-icon style="margin-right: 8px;"><Clock /></el-icon>
                <span>最近训练任务</span>
              </div>
              <el-button text @click="goTo('/training')">查看全部</el-button>
            </div>
          </template>
          <el-table :data="recentTasks" style="width: 100%">
            <el-table-column prop="name" label="任务名称" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="progress" label="进度" width="100">
              <template #default="{ row }">
                <span>{{ row.progress }}%</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header>
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <div>
                <el-icon style="margin-right: 8px;"><TrendCharts /></el-icon>
                <span>系统状态</span>
              </div>
            </div>
          </template>
          <div style="padding: 20px 0;">
            <el-row :gutter="20">
              <el-col :span="12">
                <div style="text-align: center; padding: 20px;">
                  <el-icon :size="40" color="#67c23a"><CircleCheck /></el-icon>
                  <div style="margin-top: 10px; font-size: 14px; color: #666;">系统运行正常</div>
                </div>
              </el-col>
              <el-col :span="12">
                <div style="text-align: center; padding: 20px;">
                  <el-icon :size="40" color="#409eff"><DataAnalysis /></el-icon>
                  <div style="margin-top: 10px; font-size: 14px; color: #666;">数据库连接正常</div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { modelsAPI, datasetsAPI, trainingAPI } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()

const stats = ref({
  totalModels: 0,
  totalDatasets: 0,
  totalTasks: 0,
  runningTasks: 0
})

const recentTasks = ref([])

const loadStats = async () => {
  try {
    const [models, datasets, tasks] = await Promise.all([
      modelsAPI.getAll(),
      datasetsAPI.getAll(),
      trainingAPI.getTasks()
    ])
    
    stats.value.totalModels = models.length
    stats.value.totalDatasets = datasets.length
    stats.value.totalTasks = tasks.length
    stats.value.runningTasks = tasks.filter(t => t.status === 'running').length
    
    // Get recent tasks (last 5)
    recentTasks.value = tasks.slice(0, 5).map(task => ({
      name: task.name,
      status: task.status,
      progress: task.progress || 0
    }))
  } catch (error) {
    ElMessage.error('加载统计数据失败: ' + error.message)
  }
}

const goTo = (path) => {
  router.push(path)
}

const getStatusType = (status) => {
  const typeMap = {
    'pending': 'info',
    'running': 'warning',
    'completed': 'success',
    'failed': 'danger'
  }
  return typeMap[status] || 'info'
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.stat-card {
  color: white;
}

.stat-card :deep(.el-card__body) {
  padding: 20px;
}
</style>
