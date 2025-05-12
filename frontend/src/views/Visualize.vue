<template>
  <div class="visualize-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>数据可视化 - {{ filename }}</span>
        </div>
      </template>
      
      <div class="form-container">
        <el-form :model="chartForm" label-width="120px">
          <el-form-item label="图表类型">
            <el-select v-model="chartForm.chartType" placeholder="请选择图表类型">
              <el-option label="折线图" value="line"></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="X轴列">
            <el-select v-model="chartForm.xColumn" placeholder="请选择X轴列">
              <el-option 
                v-for="column in columns" 
                :key="column" 
                :label="column" 
                :value="column">
              </el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="Y轴列">
            <el-select 
              v-model="chartForm.yColumns" 
              multiple 
              placeholder="请选择Y轴列(可多选)">
              <el-option 
                v-for="column in columns" 
                :key="column" 
                :label="column" 
                :value="column">
              </el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="图表标题">
            <el-input v-model="chartForm.title" placeholder="请输入图表标题"></el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="generateChart">生成图表</el-button>
            <el-button @click="goBack">返回</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 图表容器 -->
      <div v-loading="loading" class="chart-container">
        <div v-if="noDataSelected" class="no-data-tip">
          请选择数据列并生成图表
        </div>
        <div v-else-if="chartError" class="error-tip">
          {{ chartError }}
        </div>
        <div v-else id="chartArea" style="width: 100%; height: 400px;"></div>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  name: 'Visualize',
  data() {
    return {
      filename: this.$route.params.filename,
      columns: [],
      chartForm: {
        chartType: 'line',
        xColumn: '',
        yColumns: [],
        title: '数据折线图'
      },
      loading: false,
      chartError: '',
      chartInstance: null
    }
  },
  computed: {
    noDataSelected() {
      return !this.chartForm.xColumn || this.chartForm.yColumns.length === 0;
    }
  },
  mounted() {
    this.fetchColumns();
    // 添加窗口大小变化监听，以便重新调整图表大小
    window.addEventListener('resize', this.resizeChart);
  },
  beforeUnmount() {
    // 组件卸载前移除事件监听和销毁图表实例
    window.removeEventListener('resize', this.resizeChart);
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
  },
  methods: {
    // 获取数据列
    fetchColumns() {
      this.loading = true;
      axios.get(`http://localhost:5000/api/preview/${this.filename}`)
        .then(response => {
          if (response.data.success) {
            this.columns = response.data.info.column_names;
          } else {
            this.chartError = '获取数据列失败';
          }
        })
        .catch(error => {
          console.error('获取数据列出错:', error);
          this.chartError = `获取数据列出错: ${error.message}`;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    // 生成图表
    generateChart() {
      if (this.noDataSelected) {
        this.chartError = '请先选择X轴和Y轴数据列';
        return;
      }
      
      this.loading = true;
      this.chartError = '';
      
      const params = {
        filename: this.filename,
        x_column: this.chartForm.xColumn,
        y_columns: this.chartForm.yColumns,
        title: this.chartForm.title,
        xaxis_title: this.chartForm.xColumn,
        yaxis_title: '数值'
      };
      
      axios.post('http://localhost:5000/api/visualize/line', params)
        .then(response => {
          if (response.data.success) {
            this.renderChart(response.data.chart_data);
          } else {
            this.chartError = '生成图表失败';
          }
        })
        .catch(error => {
          console.error('生成图表出错:', error);
          this.chartError = `生成图表出错: ${error.message}`;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    // 渲染图表
    renderChart(chartData) {
      // 确保图表容器存在
      const chartDom = document.getElementById('chartArea');
      if (!chartDom) {
        console.error('找不到图表容器');
        return;
      }
      
      // 如果已经有实例，先销毁
      if (this.chartInstance) {
        this.chartInstance.dispose();
      }
      
      // 创建新的图表实例
      this.chartInstance = echarts.init(chartDom);
      
      // 转换Plotly数据到ECharts格式
      const series = [];
      
      try {
        // 处理从Plotly转换到ECharts的数据
        const traces = chartData.data || [];
        
        traces.forEach(trace => {
          series.push({
            name: trace.name,
            type: 'line',
            data: trace.y.map((y, index) => [trace.x[index], y]),
            showSymbol: true,
            smooth: true
          });
        });
        
        const option = {
          title: {
            text: this.chartForm.title
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: series.map(item => item.name)
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            name: this.chartForm.xColumn,
            boundaryGap: false,
            data: chartData.data[0]?.x || []
          },
          yAxis: {
            type: 'value',
            name: '数值'
          },
          series: series
        };
        
        // 设置图表配置
        this.chartInstance.setOption(option);
      } catch (error) {
        console.error('渲染图表出错:', error);
        this.chartError = `渲染图表出错: ${error.message}`;
      }
    },
    
    // 调整图表大小
    resizeChart() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    },
    
    // 返回按钮
    goBack() {
      this.$router.push('/preview/' + this.filename);
    }
  }
}
</script>

<style scoped>
.visualize-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.form-container {
  margin-bottom: 20px;
}

.chart-container {
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.no-data-tip, .error-tip {
  text-align: center;
  color: #909399;
  font-size: 16px;
  padding: 40px 0;
}

.error-tip {
  color: #f56c6c;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
