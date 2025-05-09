import Vue from 'vue'
import VueRouter from 'vue-router'

// 将在此处导入视图组件
// import Home from '@/views/Home.vue'

Vue.use(VueRouter)

const routes = [
  // 在此处定义路由
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: Home
  // }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router 