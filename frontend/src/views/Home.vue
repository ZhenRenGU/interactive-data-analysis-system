<template>
  <div class="home">
    <h1>交互式数据分析系统</h1>
    <!-- 此处添加首页内容 -->

    <!-- 文件上传区域 -->
    <div class="upload-section">
      <h2>上传数据文件</h2>
      <el-upload
        class="upload-demo"
        drag
        action="http://localhost:5000/api/upload"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload">

        <!-- 上传区域内容 -->
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">支持上传 CSV, Excel 格式文件</div>
      </el-upload>
    </div>

    <div v-if="existingFiles.length > 0" class="existing-files">
      <h2>已上传的文件</h2>
      <el-table :data="existingFiles" style="width: 100%">
        <el-table-column prop="filename" label="文件名"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button 
              size="mini" 
              @click="previewFile(scope.row.filename)">预览</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

  </div>
</template>

<script>
// 导入axios
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    // 在此导入和注册组件
  },
  data() {
    return {
      // 组件数据
      existingFiles: [],
    }
  },
  created() {
    this.fetchExistingFiles()
  },
  methods: {
    // 组件方法
    // 获取已上传的文件列表
    fetchExistingFiles() {
      axios.get('http://localhost:5000/api/files')
        .then(response => {
          this.existingFiles = response.data.files.map(filename => ({ filename }))
        })
        .catch(error => {
          this.$message.error('获取文件列表失败: ' + error.message)
        })
    },

    handleUploadSuccess(response) {
      this.$message.success('文件上传成功')
      this.fetchExistingFiles()
    },

    handleUploadError(err) {
      this.$message.error('文件上传失败: ' + err.message)
    },

    beforeUpload(file) {
      const isValidType = ['text/csv', 'application/vnd.ms-excel', 
                           'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'].includes(file.type)
      if (!isValidType) {
        this.$message.error('只能上传CSV或Excel文件!')
        return false
      }
      return true
    },
    previewFile(filename) {
      this.$router.push(`/preview/${filename}`)
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}
.upload-section {
  margin: 30px 0;
}
.existing-files {
  margin-top: 40px;
}
</style>