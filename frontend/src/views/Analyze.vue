<template>
  <div class="analyze-container">
    <el-card class="box-card">
      <template #header>
        <div class="clearfix">
          <span>数据分析</span>
        </div>
      </template>
      <div class="content">
        <p>正在开发数据分析功能，敬请期待...</p>
        <el-button type="primary" @click="goBack">返回</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const filename = ref(route.params.filename)

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
.content {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
