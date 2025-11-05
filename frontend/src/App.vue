<template>
  <el-config-provider :locale="locale">
    <div id="app">
      <el-container class="layout-container">
        <!-- 侧边栏 -->
        <el-aside width="220px" class="sidebar">
          <div class="logo">
            <el-icon :size="32"><Grid /></el-icon>
            <h2>VulWeb</h2>
          </div>
          <el-menu
            :default-active="activeMenu"
            class="sidebar-menu"
            router
            @select="handleMenuSelect"
          >
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>首页Dashboard</span>
            </el-menu-item>
            <el-menu-item index="/models">
              <el-icon><Box /></el-icon>
              <span>模型管理</span>
            </el-menu-item>
            <el-menu-item index="/datasets">
              <el-icon><Folder /></el-icon>
              <span>数据集管理</span>
            </el-menu-item>
            <el-menu-item index="/training">
              <el-icon><Connection /></el-icon>
              <span>训练任务</span>
            </el-menu-item>
            <el-menu-item index="/results">
              <el-icon><TrendCharts /></el-icon>
              <span>结果展示</span>
            </el-menu-item>
            <el-menu-item index="/chat">
              <el-icon><ChatDotRound /></el-icon>
              <span>AI对话</span>
            </el-menu-item>
            <el-menu-item index="/settings">
              <el-icon><Setting /></el-icon>
              <span>系统设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <!-- 主内容区 -->
        <el-container>
          <el-header class="header">
            <div class="header-content">
              <h3>代码漏洞检测模型管理系统</h3>
              <div class="header-actions">
                <el-button text @click="toggleDark">
                  <el-icon><Moon v-if="!isDark" /><Sunny v-else /></el-icon>
                </el-button>
              </div>
            </div>
          </el-header>
          <el-main class="main-content">
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </el-main>
        </el-container>
      </el-container>
    </div>
  </el-config-provider>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const route = useRoute()
const locale = ref(zhCn)
const isDark = ref(false)

const activeMenu = computed(() => route.path)

const handleMenuSelect = (index) => {
  console.log('Menu selected:', index)
}

const toggleDark = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

onMounted(() => {
  // Check for saved theme preference or default to light mode
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 
               'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  overflow: hidden;
}

.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  color: #fff;
  overflow-y: auto;
}

.logo {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo .el-icon {
  color: #409EFF;
  margin-right: 12px;
}

.logo h2 {
  color: #fff;
  font-size: 20px;
  font-weight: 600;
}

.sidebar-menu {
  border: none;
  background-color: transparent;
}

.sidebar-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.7);
}

.sidebar-menu .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.sidebar-menu .el-menu-item.is-active {
  background-color: #409EFF !important;
  color: #fff !important;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h3 {
  color: #333;
  font-size: 18px;
  font-weight: 500;
}

.main-content {
  background-color: #f0f2f5;
  overflow-y: auto;
  padding: 20px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Dark mode */
.dark .header {
  background-color: #1a1a1a;
  border-bottom-color: #333;
}

.dark .header-content h3 {
  color: #fff;
}

.dark .main-content {
  background-color: #141414;
}
</style>
