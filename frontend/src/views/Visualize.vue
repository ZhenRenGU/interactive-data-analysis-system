<template>
  <div class="visualize-container">
    <el-card class="box-card">
      <template #header>
        <div class="clearfix">
          <span>数据可视化</span>
        </div>
      </template>
      <div class="content">
        <p>正在开发数据可视化功能，敬请期待...</p>
        <el-button type="primary" @click="goBack">返回</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Visualize',
  data() {
    return {
      filename: this.$route.params.filename
    }
  },
  methods: {
    goBack() {
      this.$router.push('/preview/' + this.filename)
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
.content {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
