import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '首页Dashboard' }
  },
  {
    path: '/models',
    name: 'Models',
    component: () => import('@/views/Models.vue'),
    meta: { title: '模型管理' }
  },
  {
    path: '/datasets',
    name: 'Datasets',
    component: () => import('@/views/Datasets.vue'),
    meta: { title: '数据集管理' }
  },
  {
    path: '/training',
    name: 'Training',
    component: () => import('@/views/Training.vue'),
    meta: { title: '训练任务' }
  },
  {
    path: '/results',
    name: 'Results',
    component: () => import('@/views/Results.vue'),
    meta: { title: '结果展示' }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: { title: 'AI对话' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { title: '系统设置' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - VulWeb` : 'VulWeb'
  next()
})

export default router
