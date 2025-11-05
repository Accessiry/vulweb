<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">数据集管理</h2>
      <el-button type="primary" @click="showUploadDialog = true">
        <el-icon><FolderAdd /></el-icon>
        上传数据集
      </el-button>
    </div>

    <!-- 数据集列表 -->
    <div class="card-grid">
      <el-card v-for="dataset in datasets" :key="dataset.id" shadow="hover">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">{{ dataset.name }}</span>
            <el-button
              type="danger"
              text
              @click="deleteDataset(dataset.id)"
              :icon="Delete"
            />
          </div>
        </template>
        <div>
          <el-descriptions :column="1" size="small">
            <el-descriptions-item label="描述">
              {{ dataset.description || '无' }}
            </el-descriptions-item>
            <el-descriptions-item label="格式">
              <el-tag size="small">{{ dataset.format || '未知' }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="文件大小">
              {{ formatFileSize(dataset.size) }}
            </el-descriptions-item>
            <el-descriptions-item label="样本数">
              <span style="font-weight: bold; color: #409eff;">
                {{ dataset.num_samples || 0 }}
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="漏洞/安全">
              <span style="color: #f56c6c;">{{ dataset.num_vulnerable || 0 }}</span>
              /
              <span style="color: #67c23a;">{{ dataset.num_safe || 0 }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="预处理状态">
              <el-tag :type="getStatusType(dataset.preprocessing_status)" size="small">
                {{ getStatusText(dataset.preprocessing_status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="上传时间">
              {{ formatDate(dataset.created_at) }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </el-card>

      <!-- 空状态 -->
      <el-empty v-if="datasets.length === 0" description="暂无数据集，请先上传" />
    </div>

    <!-- 上传对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传数据集"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="数据集名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入数据集名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入数据集描述"
          />
        </el-form-item>
        <el-form-item label="数据集文件" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :file-list="fileList"
            accept=".json,.csv,.txt,.zip"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div style="color: #909399; font-size: 12px; margin-top: 8px;">
                支持 .json, .csv, .txt, .zip 格式，文件大小不超过 500MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="uploadDataset" :loading="uploading">
          上传
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { datasetsAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'

const datasets = ref([])
const showUploadDialog = ref(false)
const uploading = ref(false)
const formRef = ref(null)
const uploadRef = ref(null)
const fileList = ref([])

const form = ref({
  name: '',
  description: '',
  file: null
})

const rules = {
  name: [{ required: true, message: '请输入数据集名称', trigger: 'blur' }],
  file: [{ required: true, message: '请选择数据集文件', trigger: 'change' }]
}

const loadDatasets = async () => {
  try {
    datasets.value = await datasetsAPI.getAll()
  } catch (error) {
    ElMessage.error('加载数据集列表失败: ' + error.message)
  }
}

const handleFileChange = (file) => {
  form.value.file = file.raw
  fileList.value = [file]
}

const uploadDataset = async () => {
  try {
    await formRef.value.validate()
    
    uploading.value = true
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('description', form.value.description)
    formData.append('file', form.value.file)

    await datasetsAPI.upload(formData)
    ElMessage.success('数据集上传成功')
    showUploadDialog.value = false
    resetForm()
    loadDatasets()
  } catch (error) {
    ElMessage.error('上传失败: ' + error.message)
  } finally {
    uploading.value = false
  }
}

const deleteDataset = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除此数据集吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await datasetsAPI.delete(id)
    ElMessage.success('数据集删除成功')
    loadDatasets()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + error.message)
    }
  }
}

const resetForm = () => {
  formRef.value?.resetFields()
  form.value = {
    name: '',
    description: '',
    file: null
  }
  fileList.value = []
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const getStatusType = (status) => {
  const typeMap = {
    'pending': 'info',
    'processing': 'warning',
    'completed': 'success',
    'failed': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'failed': '失败'
  }
  return textMap[status] || status
}

onMounted(() => {
  loadDatasets()
})
</script>
