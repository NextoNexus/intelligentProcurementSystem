<template>
  <div class="flex h-screen">
    <!-- 左侧菜单栏 -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <!-- Logo区域 -->
      <div class="p-6 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-primary-600 rounded-lg"></div>
          <div>
            <h1 class="text-lg font-bold text-gray-900">智能采购系统</h1>
            <p class="text-xs text-gray-500">Intelligent Procurement</p>
          </div>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="flex-1 p-4 overflow-y-auto">
        <div class="space-y-2">
          <div v-for="item in menuItems" :key="item.id">
            <router-link
              :to="item.path"
              class="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-primary-50 hover:text-primary-700 transition-colors"
              :class="{ 'bg-primary-50 text-primary-700': $route.path.startsWith(item.path) }"
            >
              <span class="text-lg">{{ item.icon }}</span>
              <span class="font-medium">{{ item.label }}</span>
            </router-link>
          </div>
        </div>

        <!-- 用户信息 -->
        <div v-if="false" class="mt-auto pt-6 border-t border-gray-200">
          <div class="flex items-center space-x-3 px-4 py-3">
            <div class="w-10 h-10 bg-gradient-to-r from-primary-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold">
              {{ userInitial }}
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">{{ userFullName.value }}</p>
              <p class="text-xs text-gray-500">{{ userRole.value }}</p>
            </div>
            <button
              @click="handleLogout"
              class="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-100"
              title="退出登录"
            >
              <span class="text-lg">🚪</span>
            </button>
          </div>
        </div>
      </nav>
    </aside>

    <!-- 中间主内容区 -->
    <main class="flex-1 overflow-y-auto p-6">
      <div class="max-w-7xl mx-auto">
        <router-view />
      </div>
    </main>

    <!-- 右侧AI聊天栏 -->
    <aside v-if="false" class="w-80 bg-white border-l border-gray-200 flex flex-col">
      <!-- AI聊天头部 -->
      <div class="p-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-gradient-to-r from-primary-500 to-purple-500 rounded-lg"></div>
            <div>
              <h2 class="font-bold text-gray-900">AI助手</h2>
              <p class="text-xs text-gray-500">智能采购顾问</p>
            </div>
          </div>
          <button class="text-gray-400 hover:text-gray-600">
            <span class="text-xl">⚙️</span>
          </button>
        </div>
      </div>

      <!-- 聊天消息区域 -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4">
        <div class="text-center text-gray-500 text-sm py-8">
          <p>👋 您好！我是您的采购助手</p>
          <p class="mt-1">请问有什么可以帮您？</p>
        </div>
      </div>

      <!-- 聊天输入区域 -->
      <div class="p-4 border-t border-gray-200">
        <div class="relative">
          <input
            type="text"
            placeholder="输入您的问题..."
            class="w-full px-4 py-3 pr-12 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <button class="absolute right-3 top-3 text-primary-600 hover:text-primary-800">
            <span class="text-xl">📤</span>
          </button>
        </div>
        <p class="text-xs text-gray-500 mt-2 text-center">
          支持文本聊天和只读数据库查询
        </p>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

onMounted(() => {
  console.log('MainLayout mounted')
  console.log('authStore.user:', authStore.user)
  console.log('authStore.userInfo:', authStore.userInfo)
  console.log('userFullName.value:', userFullName.value)
  console.log('userRole.value:', userRole.value)
})

const menuItems = ref([
  { id: 1, label: '仪表盘', path: '/dashboard', icon: '📊' },
  { id: 2, label: '供应商管理', path: '/suppliers', icon: '🏢' },
  { id: 3, label: '采购管理', path: '/procurement', icon: '📦' },
  { id: 4, label: '库存管理', path: '/inventory', icon: '📋' },
  { id: 5, label: '财务管理', path: '/finance', icon: '💰' },
  { id: 6, label: '报表分析', path: '/analytics', icon: '📈' },
  { id: 7, label: '用户管理', path: '/users', icon: '👥' },
])

const userInfo = computed(() => authStore.userInfo)
const userFullName = computed(() => userInfo.value?.fullName || userInfo.value?.username || '当前用户')
const userRole = computed(() => {
  const roles = authStore.userRoles
  if (roles.includes('admin')) return '管理员'
  if (roles.includes('department_head')) return '部门主管'
  if (roles.includes('management')) return '管理层'
  if (roles.includes('employee')) return '员工'
  return '员工'
})

const userInitial = computed(() => {
  const name = userFullName.value
  if (!name || typeof name !== 'string') return 'U'
  const firstChar = name.charAt ? name.charAt(0) : ''
  return firstChar ? firstChar.toUpperCase() : 'U'
})

const handleLogout = () => {
  authStore.logout()
}
</script>

<style scoped>
.router-link-active {
  @apply bg-primary-50 text-primary-700;
}
</style>