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
        
        <!-- 数据清洗选项 -->
        <div class="clean-options-section">
          <h2>数据清洗选项</h2>
          <el-collapse v-model="activeCollapse">
            <!-- 缺失值处理 -->
            <el-collapse-item title="缺失值处理" name="missing">
              <el-form :model="cleanOptions.missingValues" label-width="120px">
                <el-form-item label="处理策略">
                  <el-select v-model="cleanOptions.missingValues.strategy" placeholder="选择处理策略">
                    <el-option label="删除缺失值" value="drop"></el-option>
                    <el-option label="均值填充" value="mean"></el-option>
                    <el-option label="中位数填充" value="median"></el-option>
                    <el-option label="众数填充" value="mode"></el-option>
                    <el-option label="固定值填充" value="value"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item v-if="cleanOptions.missingValues.strategy === 'value'" label="填充值">
                  <el-input v-model="cleanOptions.missingValues.fillValue" placeholder="请输入填充值"></el-input>
                </el-form-item>
                <el-form-item label="应用的列">
                  <el-select v-model="cleanOptions.missingValues.columns" multiple placeholder="选择要处理的列(默认全部)">
                    <el-option 
                      v-for="column in dataInfo.column_names" 
                      :key="column" 
                      :label="column" 
                      :value="column">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-form>
            </el-collapse-item>
            
            <!-- 异常值处理 -->
            <el-collapse-item title="异常值处理" name="outliers">
              <el-form :model="cleanOptions.outliers" label-width="120px">
                <el-form-item label="检测方法">
                  <el-select v-model="cleanOptions.outliers.method" placeholder="选择检测方法">
                    <el-option label="Z-Score法" value="zscore"></el-option>
                    <el-option label="IQR法" value="iqr"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item v-if="cleanOptions.outliers.method === 'zscore'" label="阈值">
                  <el-input-number v-model="cleanOptions.outliers.threshold" :min="1" :max="5" :step="0.5"></el-input-number>
                </el-form-item>
                <el-form-item label="是否删除异常值">
                  <el-switch v-model="cleanOptions.outliers.remove"></el-switch>
                </el-form-item>
              </el-form>
            </el-collapse-item>
            
            <!-- 数据标准化 -->
            <el-collapse-item title="数据标准化" name="normalize">
              <el-form :model="cleanOptions.normalize" label-width="120px">
                <el-form-item label="标准化方法">
                  <el-select v-model="cleanOptions.normalize.method" placeholder="选择标准化方法">
                    <el-option label="最小最大归一化" value="minmax"></el-option>
                    <el-option label="Z-Score标准化" value="zscore"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="应用的列">
                  <el-select v-model="cleanOptions.normalize.columns" multiple placeholder="选择要处理的列(默认所有数值列)">
                    <el-option 
                      v-for="column in numericColumns" 
                      :key="column" 
                      :label="column" 
                      :value="column">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-form>
            </el-collapse-item>
          </el-collapse>
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
          <el-dropdown @command="handleExport" split-button type="warning">
            导出数据
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="csv">导出为CSV</el-dropdown-item>
                <el-dropdown-item command="excel">导出为Excel</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
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
const activeCollapse = ref([]) // 控制折叠面板的打开状态
const dataInfo = ref({
  rows: 0,
  columns: 0,
  column_names: [],
  dtypes: {},
  missing_values: {},
  preview: []
})

// 数据清洗选项
const cleanOptions = ref({
  missingValues: {
    strategy: 'drop',
    columns: [],
    fillValue: ''
  },
  outliers: {
    method: 'zscore',
    threshold: 3,
    remove: false
  },
  normalize: {
    method: 'minmax',
    columns: []
  }
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

// 计算数值型列
const numericColumns = computed(() => {
  if (!dataInfo.value.dtypes) return []
  
  return dataInfo.value.column_names.filter(col => {
    const type = dataInfo.value.dtypes[col] || ''
    return type.includes('int') || type.includes('float')
  })
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

// 导出数据
const handleExport = (command) => {
  // 创建下载链接
  const downloadUrl = `http://localhost:5000/api/export?filename=${filename.value}&format=${command}`
  
  // 打开下载链接
  window.open(downloadUrl, '_blank')
  
  ElMessage.success(`正在导出${command.toUpperCase()}文件`)
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
.info-section, .missing-values-section, .clean-options-section, .data-preview-section {
  margin-bottom: 30px;
}
.actions {
  margin-top: 30px;
  display: flex;
  gap: 10px;
}
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 50px 0;
}
</style>