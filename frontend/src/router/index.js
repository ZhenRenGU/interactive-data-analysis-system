import Vue from 'vue'
import VueRouter from 'vue-router'


// 将在此处导入视图组件
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  // 在此处定义路由
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
    path: '/analysis/:filename',
    name: 'Analysis',
    component: () => import('../views/Analysis.vue')
   },

   // 数据可视化
   {
    path: 'visuallize/:filename',
    name: 'Visuallize',
    component: () => import('../views/Visuallize.vue')
   }

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router 