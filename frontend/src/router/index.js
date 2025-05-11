import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  
  // 数据预览
  {
    path: '/preview/:filename',
    name: 'Preview',
    component: () => import('../views/Preview.vue')
  },
 
  // 数据分析
  {
    path: '/analyze/:filename',
    name: 'Analyze',
    component: () => import('../views/Analyze.vue')
  },

  // 数据可视化
  {
    path: '/visualize/:filename',
    name: 'Visualize',
    component: () => import('../views/Visualize.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),  // 使用 History 模式
  routes                                           // 注入定义的路由规则
})

export default router