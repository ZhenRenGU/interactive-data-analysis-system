<template>
  <div class="preview">
    <h1>数据预览: {{ filename }}</h1>
    
    <div v-loading="loading" class="loading-container">
      <p v-if="loading">正在加载数据...</p>
      
      <div v-else>
        <div class="info-section">
          <h2>数据集信息</h2>
          <el-descriptions border>
            <el-descriptions-item label="行数">{{ dataInfo.rows }}</el-descriptions-item>
            <el-descriptions-item label="列数">{{ dataInfo.columns }}</el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="missing-values-section">
          <h2>缺失值情况</h2>
          <el-table :data="missingValuesData" style="width: 100%">
            <el-table-column prop="column" label="列名"></el-table-column>
            <el-table-column prop="count" label="缺失值数量"></el-table-column>
            <el-table-column prop="percentage" label="缺失比例"></el-table-column>
          </el-table>
        </div>
        
        <div class="data-preview-section">
          <h2>数据预览</h2>
          <el-table :data="dataInfo.preview" style="width: 100%">
            <el-table-column
              v-for="column in dataInfo.column_names"
              :key="column"
              :prop="column"
              :label="column">
            </el-table-column>
          </el-table>
        </div>
        
        <div class="actions">
          <el-button type="primary" @click="goToAnalyze">进行数据分析</el-button>
          <el-button type="success" @click="goToVisualize">数据可视化</el-button>
          <el-button @click="goBack">返回</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const filename = ref(route.params.filename)
const loading = ref(true)
const dataInfo = ref({
  rows: 0,
  columns: 0,
  column_names: [],
  dtypes: {},
  missing_values: {},
  preview: []
})

// 计算缺失值数据
const missingValuesData = computed(() => {
  if (!dataInfo.value.missing_values || !dataInfo.value.rows) return []
  
  return Object.entries(dataInfo.value.missing_values).map(([column, count]) => ({
    column,
    count,
    percentage: ((count / dataInfo.value.rows) * 100).toFixed(2) + '%'
  }))
})

onMounted(() => {
  fetchPreviewData()
})

// 获取数据预览
const fetchPreviewData = () => {
  loading.value = true
  axios.get(`http://localhost:5000/api/preview/${filename.value}`)
    .then(response => {
      dataInfo.value = response.data.info
      loading.value = false
    })
    .catch(error => {
      ElMessage.error('获取数据预览失败: ' + error.message)
      loading.value = false
    })
}

const goToAnalyze = () => {
  router.push(`/analyze/${filename.value}`)
}

const goToVisualize = () => {
  router.push(`/visualize/${filename.value}`)
}

const goBack = () => {
  router.push('/')
}
</script>

<style scoped>
.preview {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
.info-section, .missing-values-section, .data-preview-section {
  margin-bottom: 30px;
}
.actions {
  margin-top: 30px;
}
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 50px 0;
}
</style>