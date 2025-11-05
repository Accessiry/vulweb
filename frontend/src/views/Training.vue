<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">训练任务</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><VideoPlay /></el-icon>
        创建训练任务
      </el-button>
    </div>

    <!-- 训练任务列表 -->
    <el-table :data="tasks" style="width: 100%;">
      <el-table-column prop="name" label="任务名称" width="180" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="progress" label="进度" width="150">
        <template #default="{ row }">
          <el-progress :percentage="row.progress || 0" />
        </template>
      </el-table-column>
      <el-table-column prop="current_epoch" label="当前轮次" width="100">
        <template #default="{ row }">
          {{ row.current_epoch || 0 }} / {{ row.total_epochs || 0 }}
        </template>
      </el-table-column>
      <el-table-column prop="accuracy" label="准确率" width="100">
        <template #default="{ row }">
          <span v-if="row.accuracy">{{ (row.accuracy * 100).toFixed(2) }}%</span>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'running'"
            type="warning"
            size="small"
            @click="stopTask(row.id)"
          >
            停止
          </el-button>
          <el-button
            type="primary"
            size="small"
            @click="viewMetrics(row)"
          >
            查看
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="deleteTask(row.id)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建训练任务对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="创建训练任务"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="选择模型" prop="model_id">
          <el-select v-model="form.model_id" placeholder="请选择模型" style="width: 100%;">
            <el-option
              v-for="model in models"
              :key="model.id"
              :label="model.name"
              :value="model.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="选择数据集" prop="dataset_id">
          <el-select v-model="form.dataset_id" placeholder="请选择数据集" style="width: 100%;">
            <el-option
              v-for="dataset in datasets"
              :key="dataset.id"
              :label="dataset.name"
              :value="dataset.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="训练轮次" prop="total_epochs">
          <el-input-number v-model="form.total_epochs" :min="1" :max="1000" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createTask" :loading="creating">
          创建并开始训练
        </el-button>
      </template>
    </el-dialog>

    <!-- 指标查看对话框 -->
    <el-dialog
      v-model="showMetricsDialog"
      :title="`训练指标 - ${currentTask?.name}`"
      width="900px"
    >
      <div v-if="currentTask">
        <!-- 当前指标卡片 -->
        <el-row :gutter="20" style="margin-bottom: 20px;">
          <el-col :span="6">
            <el-card>
              <div style="text-align: center;">
                <div style="font-size: 12px; color: #909399; margin-bottom: 8px;">Loss</div>
                <div style="font-size: 24px; font-weight: bold; color: #409eff;">
                  {{ currentTask.loss?.toFixed(4) || '-' }}
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card>
              <div style="text-align: center;">
                <div style="font-size: 12px; color: #909399; margin-bottom: 8px;">Accuracy</div>
                <div style="font-size: 24px; font-weight: bold; color: #67c23a;">
                  {{ currentTask.accuracy ? (currentTask.accuracy * 100).toFixed(2) + '%' : '-' }}
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card>
              <div style="text-align: center;">
                <div style="font-size: 12px; color: #909399; margin-bottom: 8px;">Val Loss</div>
                <div style="font-size: 24px; font-weight: bold; color: #e6a23c;">
                  {{ currentTask.validation_loss?.toFixed(4) || '-' }}
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card>
              <div style="text-align: center;">
                <div style="font-size: 12px; color: #909399; margin-bottom: 8px;">Val Accuracy</div>
                <div style="font-size: 24px; font-weight: bold; color: #f56c6c;">
                  {{ currentTask.validation_accuracy ? (currentTask.validation_accuracy * 100).toFixed(2) + '%' : '-' }}
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 图表 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card>
              <template #header>Loss 趋势</template>
              <v-chart :option="lossChartOption" style="height: 300px;" />
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>Accuracy 趋势</template>
              <v-chart :option="accuracyChartOption" style="height: 300px;" />
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { modelsAPI, datasetsAPI, trainingAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
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

const tasks = ref([])
const models = ref([])
const datasets = ref([])
const showCreateDialog = ref(false)
const showMetricsDialog = ref(false)
const creating = ref(false)
const formRef = ref(null)
const currentTask = ref(null)
const metrics = ref([])

const form = ref({
  name: '',
  model_id: null,
  dataset_id: null,
  total_epochs: 10
})

const rules = {
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  model_id: [{ required: true, message: '请选择模型', trigger: 'change' }],
  dataset_id: [{ required: true, message: '请选择数据集', trigger: 'change' }],
  total_epochs: [{ required: true, message: '请输入训练轮次', trigger: 'blur' }]
}

const lossChartOption = computed(() => ({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Train Loss', 'Val Loss']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: metrics.value.map(m => m.epoch)
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Train Loss',
      type: 'line',
      data: metrics.value.map(m => m.loss),
      smooth: true,
      itemStyle: { color: '#409eff' }
    },
    {
      name: 'Val Loss',
      type: 'line',
      data: metrics.value.map(m => m.validation_loss),
      smooth: true,
      itemStyle: { color: '#e6a23c' }
    }
  ]
}))

const accuracyChartOption = computed(() => ({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Train Accuracy', 'Val Accuracy']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: metrics.value.map(m => m.epoch)
  },
  yAxis: {
    type: 'value',
    max: 1
  },
  series: [
    {
      name: 'Train Accuracy',
      type: 'line',
      data: metrics.value.map(m => m.accuracy),
      smooth: true,
      itemStyle: { color: '#67c23a' }
    },
    {
      name: 'Val Accuracy',
      type: 'line',
      data: metrics.value.map(m => m.validation_accuracy),
      smooth: true,
      itemStyle: { color: '#f56c6c' }
    }
  ]
}))

const loadTasks = async () => {
  try {
    tasks.value = await trainingAPI.getTasks()
  } catch (error) {
    ElMessage.error('加载任务列表失败: ' + error.message)
  }
}

const loadModels = async () => {
  try {
    models.value = await modelsAPI.getAll()
  } catch (error) {
    ElMessage.error('加载模型列表失败: ' + error.message)
  }
}

const loadDatasets = async () => {
  try {
    datasets.value = await datasetsAPI.getAll()
  } catch (error) {
    ElMessage.error('加载数据集列表失败: ' + error.message)
  }
}

const createTask = async () => {
  try {
    await formRef.value.validate()
    creating.value = true
    await trainingAPI.createTask(form.value)
    ElMessage.success('训练任务创建成功')
    showCreateDialog.value = false
    resetForm()
    loadTasks()
  } catch (error) {
    ElMessage.error('创建失败: ' + error.message)
  } finally {
    creating.value = false
  }
}

const stopTask = async (id) => {
  try {
    await trainingAPI.stopTask(id)
    ElMessage.success('任务已停止')
    loadTasks()
  } catch (error) {
    ElMessage.error('停止失败: ' + error.message)
  }
}

const deleteTask = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除此任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await trainingAPI.deleteTask(id)
    ElMessage.success('任务删除成功')
    loadTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + error.message)
    }
  }
}

const viewMetrics = async (task) => {
  currentTask.value = task
  showMetricsDialog.value = true
  try {
    metrics.value = await trainingAPI.getMetrics(task.id)
  } catch (error) {
    ElMessage.error('加载指标失败: ' + error.message)
  }
}

const resetForm = () => {
  formRef.value?.resetFields()
  form.value = {
    name: '',
    model_id: null,
    dataset_id: null,
    total_epochs: 10
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  return new Date(dateStr).toLocaleString('zh-CN')
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

const getStatusText = (status) => {
  const textMap = {
    'pending': '等待中',
    'running': '运行中',
    'completed': '已完成',
    'failed': '失败'
  }
  return textMap[status] || status
}

onMounted(() => {
  loadTasks()
  loadModels()
  loadDatasets()
})
</script>
