<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">模型管理</h2>
      <el-button type="primary" @click="showUploadDialog = true">
        <el-icon><Upload /></el-icon>
        上传模型
      </el-button>
    </div>

    <!-- 模型列表 -->
    <div class="card-grid">
      <el-card v-for="model in models" :key="model.id" shadow="hover">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">{{ model.name }}</span>
            <el-button
              type="danger"
              text
              @click="deleteModel(model.id)"
              :icon="Delete"
            />
          </div>
        </template>
        <div>
          <el-descriptions :column="1" size="small">
            <el-descriptions-item label="描述">
              {{ model.description || '无' }}
            </el-descriptions-item>
            <el-descriptions-item label="版本">
              <el-tag size="small">{{ model.version || '1.0.0' }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="类型">
              {{ model.model_type || '未指定' }}
            </el-descriptions-item>
            <el-descriptions-item label="准确率">
              <span v-if="model.accuracy" style="color: #67c23a; font-weight: bold;">
                {{ (model.accuracy * 100).toFixed(2) }}%
              </span>
              <span v-else style="color: #909399;">未训练</span>
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ formatDate(model.created_at) }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </el-card>

      <!-- 空状态 -->
      <el-empty v-if="models.length === 0" description="暂无模型，请先上传" />
    </div>

    <!-- 上传对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传模型"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="模型名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入模型描述"
          />
        </el-form-item>
        <el-form-item label="版本" prop="version">
          <el-input v-model="form.version" placeholder="例如: 1.0.0" />
        </el-form-item>
        <el-form-item label="模型类型" prop="model_type">
          <el-select v-model="form.model_type" placeholder="请选择模型类型" style="width: 100%;">
            <el-option label="漏洞检测" value="vulnerability_detection" />
            <el-option label="细粒度定位" value="fine_grained_location" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="模型文件" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :file-list="fileList"
            accept=".pkl,.pt,.pth,.h5,.onnx"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div style="color: #909399; font-size: 12px; margin-top: 8px;">
                支持 .pkl, .pt, .pth, .h5, .onnx 格式，文件大小不超过 500MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="uploadModel" :loading="uploading">
          上传
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { modelsAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'

const models = ref([])
const showUploadDialog = ref(false)
const uploading = ref(false)
const formRef = ref(null)
const uploadRef = ref(null)
const fileList = ref([])

const form = ref({
  name: '',
  description: '',
  version: '1.0.0',
  model_type: 'vulnerability_detection',
  file: null
})

const rules = {
  name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }],
  model_type: [{ required: true, message: '请选择模型类型', trigger: 'change' }],
  file: [{ required: true, message: '请选择模型文件', trigger: 'change' }]
}

const loadModels = async () => {
  try {
    models.value = await modelsAPI.getAll()
  } catch (error) {
    ElMessage.error('加载模型列表失败: ' + error.message)
  }
}

const handleFileChange = (file) => {
  form.value.file = file.raw
  fileList.value = [file]
}

const uploadModel = async () => {
  try {
    await formRef.value.validate()
    
    uploading.value = true
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('description', form.value.description)
    formData.append('version', form.value.version)
    formData.append('model_type', form.value.model_type)
    formData.append('file', form.value.file)

    await modelsAPI.upload(formData)
    ElMessage.success('模型上传成功')
    showUploadDialog.value = false
    resetForm()
    loadModels()
  } catch (error) {
    ElMessage.error('上传失败: ' + error.message)
  } finally {
    uploading.value = false
  }
}

const deleteModel = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除此模型吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await modelsAPI.delete(id)
    ElMessage.success('模型删除成功')
    loadModels()
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
    version: '1.0.0',
    model_type: 'vulnerability_detection',
    file: null
  }
  fileList.value = []
}

const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadModels()
})
</script>
