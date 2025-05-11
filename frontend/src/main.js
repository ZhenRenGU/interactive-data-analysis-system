import { createApp } from 'vue'         // 从 Vue 3 导入创建应用的方法
import App from './App.vue'            // 导入根组件
import router from './router'          // 导入路由配置
import store from './store'            // 导入 Vuex/Pinia 状态管理
import ElementPlus from 'element-plus' // 导入 Element Plus 组件库
import 'element-plus/dist/index.css'   // 导入 Element Plus 样式
import zhCn from 'element-plus/es/locale/lang/zh-cn' // 导入中文语言包

const app = createApp(App)

app.use(ElementPlus,{
  locale: zhCn,
})
app.use(store)
app.use(router)
app.mount('#app')