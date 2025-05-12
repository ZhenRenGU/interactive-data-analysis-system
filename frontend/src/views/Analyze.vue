<template>
  <div class="analyze-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>数据分析 - {{ filename }}</span>
        </div>
      </template>
      
      <div class="form-container">
        <el-form :model="analysisForm" label-width="120px">
          <el-form-item label="分析模型">
            <el-select v-model="analysisForm.model" placeholder="请选择分析模型">
              <el-option label="线性回归" value="linear-regression"></el-option>
            </el-select>
          </el-form-item>
          
          <!-- 线性回归模型参数 -->
          <template v-if="analysisForm.model === 'linear-regression'">
            <el-form-item label="目标变量">
              <el-select v-model="analysisForm.target" placeholder="请选择预测目标">
                <el-option 
                  v-for="column in numericColumns" 
                  :key="column" 
                  :label="column" 
                  :value="column">
                </el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="特征变量">
              <el-select 
                v-model="analysisForm.features" 
                multiple 
                placeholder="请选择特征变量(可多选)">
                <el-option 
                  v-for="column in numericColumns.filter(col => col !== analysisForm.target)" 
                  :key="column" 
                  :label="column" 
                  :value="column">
                </el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="测试集比例">
              <el-slider v-model="analysisForm.testSize" :min="10" :max="40" :format-tooltip="formatTestSize"></el-slider>
            </el-form-item>
          </template>
          
          <el-form-item>
            <el-button type="primary" @click="runAnalysis" :disabled="!canRunAnalysis">运行分析</el-button>
            <el-button @click="goBack">返回</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 分析结果显示 -->
      <div v-loading="loading" class="result-container">
        <div v-if="!result && !loading" class="no-result-tip">
          请选择分析参数并运行分析
        </div>
        <div v-else-if="error" class="error-tip">
          {{ error }}
        </div>
        <div v-else-if="result" class="analysis-result">
          <h2>线性回归分析结果</h2>
          
          <!-- 回归方程 -->
          <div class="result-section">
            <h3>回归方程</h3>
            <div class="equation">{{ result.equation }}</div>
          </div>
          
          <!-- 模型评估指标 -->
          <div class="result-section">
            <h3>模型评估</h3>
            <el-descriptions border :column="2">
              <el-descriptions-item label="训练集 R²">
                {{ (result.metrics.train_r2 * 100).toFixed(2) }}%
              </el-descriptions-item>
              <el-descriptions-item label="测试集 R²">
                {{ (result.metrics.test_r2 * 100).toFixed(2) }}%
              </el-descriptions-item>
              <el-descriptions-item label="训练集 RMSE">
                {{ result.metrics.train_rmse.toFixed(4) }}
              </el-descriptions-item>
              <el-descriptions-item label="测试集 RMSE">
                {{ result.metrics.test_rmse.toFixed(4) }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
          
          <!-- 特征重要性 -->
          <div class="result-section">
            <h3>特征重要性</h3>
            <el-table :data="featureImportanceData" style="width: 100%">
              <el-table-column prop="feature" label="特征"></el-table-column>
              <el-table-column prop="coefficient" label="系数"></el-table-column>
              <el-table-column prop="importance" label="重要性">
                <template #default="scope">
                  <el-progress :percentage="scope.row.importance"></el-progress>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </el-card>
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
const loading = ref(false)
const error = ref('')
const result = ref(null)
const columns = ref([])
const dataTypes = ref({})

// 分析表单
const analysisForm = ref({
  model: 'linear-regression',
  target: '',
  features: [],
  testSize: 20 // 默认测试集比例为20%
})

// 计算数值型列
const numericColumns = computed(() => {
  return columns.value.filter(col => {
    const type = dataTypes.value[col] || ''
    return type.includes('int') || type.includes('float')
  })
})

// 格式化测试集比例
const formatTestSize = (val) => {
  return val + '%'
}

// 检查是否可以运行分析
const canRunAnalysis = computed(() => {
  if (analysisForm.value.model === 'linear-regression') {
    return analysisForm.value.target && analysisForm.value.features.length > 0
  }
  return false
})

// 特征重要性数据
const featureImportanceData = computed(() => {
  if (!result.value) return []
  
  const importanceValues = Object.values(result.value.feature_importance)
  const maxImportance = Math.max(...importanceValues)
  
  return Object.entries(result.value.coefficients).map(([feature, coefficient]) => {
    const absCoef = Math.abs(coefficient)
    const normalizedImportance = (absCoef / maxImportance) * 100
    
    return {
      feature,
      coefficient: coefficient.toFixed(4),
      importance: Math.round(normalizedImportance)
    }
  }).sort((a, b) => b.importance - a.importance)
})

onMounted(() => {
  fetchColumns()
})

// 获取列信息
const fetchColumns = () => {
  loading.value = true
  axios.get(`http://localhost:5000/api/preview/${filename.value}`)
    .then(response => {
      if (response.data.success) {
        columns.value = response.data.info.column_names
        dataTypes.value = response.data.info.dtypes
      } else {
        error.value = '获取数据列失败'
      }
    })
    .catch(err => {
      error.value = `获取数据列出错: ${err.message}`
    })
    .finally(() => {
      loading.value = false
    })
}

// 运行分析
const runAnalysis = () => {
  if (!canRunAnalysis.value) {
    ElMessage.warning('请先完成分析参数的选择')
    return
  }
  
  loading.value = true
  error.value = ''
  result.value = null
  
  const params = {
    filename: filename.value,
    features: analysisForm.value.features,
    target: analysisForm.value.target,
    test_size: analysisForm.value.testSize / 100,
    random_state: 42
  }
  
  axios.post('http://localhost:5000/api/ml/linear-regression', params)
    .then(response => {
      if (response.data.success) {
        result.value = response.data.result
        ElMessage.success('分析完成')
      } else {
        error.value = '分析失败'
        ElMessage.error('分析失败')
      }
    })
    .catch(err => {
      error.value = `分析出错: ${err.message}`
      ElMessage.error(`分析出错: ${err.message}`)
    })
    .finally(() => {
      loading.value = false
    })
}

const goBack = () => {
  router.push('/preview/' + filename.value)
}
</script>

<style scoped>
.analyze-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-container {
  margin-bottom: 20px;
}

.result-container {
  min-height: 300px;
}

.no-result-tip, .error-tip {
  text-align: center;
  color: #909399;
  font-size: 16px;
  padding: 40px 0;
}

.error-tip {
  color: #f56c6c;
}

.analysis-result {
  padding: 20px 0;
}

.result-section {
  margin-bottom: 30px;
}

.equation {
  padding: 15px;
  background-color: #f7f7f7;
  border-radius: 4px;
  font-family: monospace;
  font-size: 16px;
  overflow-x: auto;
}
</style>
