<template>
    <div class="preview">
      <h1>数据预览: {{ filename }}</h1>
      
      <div v-if="loading" class="loading">
        <el-spinner-loading></el-spinner-loading>
        <p>正在加载数据...</p>
      </div>
      
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
          <el-button @click="goBack">返回</el-button>
        </div>
      </div>
    </div>
  </template>

<script>
import axios from 'axios'

// 获取文件信息
export default {
    name: 'Preview',
    data() {
        return {
            filename: this.$route.params.filename,
            dataInfo: {
                rows: 0,
                columns: 0,
                column_names: [],
                dtypes: {},
                missing_values: {},
                preview: []
            },
            loading: true
        }
},

// 计算缺失值数据
    computed: {
        missingValuesData() {
            if (!this.dataInfo.missing_values || !this.dataInfo.rows) return []
            
            return Object.entries(this.dataInfo.missing_values).map(([column, count]) => ({
                column,
                count,
                percentage: ((count / this.dataInfo.rows) * 100).toFixed(2) + '%'
            }))
        }
  },

  // 获取数据预览
    created() {
        this.fetchPreviewData()
    },

  // 方法
     methods: {
        // 获取数据预览
        fetchPreviewData() {
            this.loading = true
            axios.get(`http://localhost:5000/api/preview/${this.filename}`)
                .then(response => {
                this.dataInfo = response.data.info
                this.loading = false
                })
                .catch(error => {
                this.$message.error('获取数据预览失败: ' + error.message)
                this.loading = false
                })
        },
        goToAnalyze() {
            this.$router.push(`/analyze/${this.filename}`)
        },
        goBack() {
        this.$router.push('/')
        }
  }
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
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 50px 0;
}
</style>