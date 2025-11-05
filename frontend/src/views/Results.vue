<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">结果展示</h2>
      <el-button @click="loadResults" :icon="Refresh">刷新</el-button>
    </div>

    <!-- 完成的训练任务 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <span>已完成的训练任务</span>
      </template>
      <el-table :data="completedTasks" style="width: 100%;">
        <el-table-column prop="name" label="任务名称" width="200" />
        <el-table-column label="模型" width="150">
          <template #default="{ row }">
            {{ getModelName(row.model_id) }}
          </template>
        </el-table-column>
        <el-table-column label="数据集" width="150">
          <template #default="{ row }">
            {{ getDatasetName(row.dataset_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="total_epochs" label="训练轮次" width="100" />
        <el-table-column label="最终准确率" width="120">
          <template #default="{ row }">
            <span style="font-weight: bold; color: #67c23a;">
              {{ row.accuracy ? (row.accuracy * 100).toFixed(2) + '%' : '-' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="训练时间" width="120">
          <template #default="{ row }">
            {{ calculateDuration(row.start_time, row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column label="完成时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      :title="`训练详情 - ${selectedTask?.name}`"
      width="900px"
    >
      <div v-if="selectedTask">
        <!-- 基本信息 -->
        <el-descriptions title="基本信息" :column="2" border style="margin-bottom: 20px;">
          <el-descriptions-item label="任务名称">
            {{ selectedTask.name }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag type="success">已完成</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="模型">
            {{ getModelName(selectedTask.model_id) }}
          </el-descriptions-item>
          <el-descriptions-item label="数据集">
            {{ getDatasetName(selectedTask.dataset_id) }}
          </el-descriptions-item>
          <el-descriptions-item label="训练轮次">
            {{ selectedTask.total_epochs }}
          </el-descriptions-item>
          <el-descriptions-item label="训练时长">
            {{ calculateDuration(selectedTask.start_time, selectedTask.end_time) }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 性能指标 -->
        <el-row :gutter="20" style="margin-bottom: 20px;">
          <el-col :span="6">
            <el-statistic title="最终Loss" :value="selectedTask.loss?.toFixed(4) || '-'" />
          </el-col>
          <el-col :span="6">
            <el-statistic 
              title="最终Accuracy" 
              :value="selectedTask.accuracy ? (selectedTask.accuracy * 100).toFixed(2) + '%' : '-'"
            />
          </el-col>
          <el-col :span="6">
            <el-statistic 
              title="验证Loss" 
              :value="selectedTask.validation_loss?.toFixed(4) || '-'"
            />
          </el-col>
          <el-col :span="6">
            <el-statistic 
              title="验证Accuracy" 
              :value="selectedTask.validation_accuracy ? (selectedTask.validation_accuracy * 100).toFixed(2) + '%' : '-'"
            />
          </el-col>
        </el-row>

        <!-- 训练曲线 -->
        <el-card>
          <template #header>训练曲线</template>
          <el-row :gutter="20">
            <el-col :span="12">
              <v-chart :option="detailLossChart" style="height: 350px;" />
            </el-col>
            <el-col :span="12">
              <v-chart :option="detailAccuracyChart" style="height: 350px;" />
            </el-col>
          </el-row>
        </el-card>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { trainingAPI, modelsAPI, datasetsAPI } from '@/api'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const completedTasks = ref([])
const models = ref([])
const datasets = ref([])
const showDetailDialog = ref(false)
const selectedTask = ref(null)
const selectedMetrics = ref([])

const loadResults = async () => {
  try {
    const [tasks, modelsData, datasetsData] = await Promise.all([
      trainingAPI.getTasks(),
      modelsAPI.getAll(),
      datasetsAPI.getAll()
    ])
    
    models.value = modelsData
    datasets.value = datasetsData
    completedTasks.value = tasks.filter(t => t.status === 'completed')
  } catch (error) {
    ElMessage.error('加载结果失败: ' + error.message)
  }
}

const viewDetail = async (task) => {
  selectedTask.value = task
  showDetailDialog.value = true
  
  try {
    selectedMetrics.value = await trainingAPI.getMetrics(task.id)
  } catch (error) {
    ElMessage.error('加载指标失败: ' + error.message)
  }
}

const getModelName = (modelId) => {
  const model = models.value.find(m => m.id === modelId)
  return model?.name || '未知'
}

const getDatasetName = (datasetId) => {
  const dataset = datasets.value.find(d => d.id === datasetId)
  return dataset?.name || '未知'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const calculateDuration = (startStr, endStr) => {
  if (!startStr || !endStr) return '-'
  const start = new Date(startStr)
  const end = new Date(endStr)
  const diff = Math.floor((end - start) / 1000) // seconds
  
  const hours = Math.floor(diff / 3600)
  const minutes = Math.floor((diff % 3600) / 60)
  const seconds = diff % 60
  
  if (hours > 0) {
    return `${hours}小时${minutes}分${seconds}秒`
  } else if (minutes > 0) {
    return `${minutes}分${seconds}秒`
  } else {
    return `${seconds}秒`
  }
}

const detailLossChart = computed(() => ({
  title: {
    text: 'Loss变化趋势',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Train Loss', 'Val Loss'],
    top: 30
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: 70,
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: selectedMetrics.value.map(m => `Epoch ${m.epoch}`)
  },
  yAxis: {
    type: 'value',
    name: 'Loss'
  },
  series: [
    {
      name: 'Train Loss',
      type: 'line',
      data: selectedMetrics.value.map(m => m.loss),
      smooth: true,
      itemStyle: { color: '#409eff' }
    },
    {
      name: 'Val Loss',
      type: 'line',
      data: selectedMetrics.value.map(m => m.validation_loss),
      smooth: true,
      itemStyle: { color: '#e6a23c' }
    }
  ]
}))

const detailAccuracyChart = computed(() => ({
  title: {
    text: 'Accuracy变化趋势',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis',
    formatter: (params) => {
      let result = params[0].axisValue + '<br/>'
      params.forEach(param => {
        result += `${param.marker}${param.seriesName}: ${(param.value * 100).toFixed(2)}%<br/>`
      })
      return result
    }
  },
  legend: {
    data: ['Train Accuracy', 'Val Accuracy'],
    top: 30
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: 70,
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: selectedMetrics.value.map(m => `Epoch ${m.epoch}`)
  },
  yAxis: {
    type: 'value',
    name: 'Accuracy',
    min: 0,
    max: 1,
    axisLabel: {
      formatter: (value) => (value * 100).toFixed(0) + '%'
    }
  },
  series: [
    {
      name: 'Train Accuracy',
      type: 'line',
      data: selectedMetrics.value.map(m => m.accuracy),
      smooth: true,
      itemStyle: { color: '#67c23a' }
    },
    {
      name: 'Val Accuracy',
      type: 'line',
      data: selectedMetrics.value.map(m => m.validation_accuracy),
      smooth: true,
      itemStyle: { color: '#f56c6c' }
    }
  ]
}))

onMounted(() => {
  loadResults()
})
</script>
