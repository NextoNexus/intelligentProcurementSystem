<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 p-4">
    <div class="text-center max-w-lg">
      <!-- 404图标 -->
      <div class="relative mb-8">
        <div class="w-48 h-48 mx-auto bg-gradient-to-br from-primary-50 to-blue-50 rounded-full flex items-center justify-center">
          <span class="text-6xl">🔍</span>
        </div>
        <div class="absolute -top-4 -right-4 w-32 h-32 bg-gradient-to-br from-yellow-50 to-orange-50 rounded-full opacity-70"></div>
        <div class="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-br from-purple-50 to-pink-50 rounded-full opacity-70"></div>
      </div>

      <!-- 错误信息 -->
      <h1 class="text-6xl font-bold text-gray-900 mb-4">404</h1>
      <h2 class="text-2xl font-bold text-gray-800 mb-4">页面未找到</h2>
      <p class="text-gray-600 mb-8">
        抱歉，您访问的页面不存在或已被移动。<br/>
        请检查URL是否正确，或返回首页继续浏览。
      </p>

      <!-- 操作按钮 -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          @click="goBack"
          class="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
        >
          ← 返回上一页
        </button>
        <button
          @click="goHome"
          class="px-6 py-3 bg-gradient-to-r from-primary-600 to-blue-600 text-white font-medium rounded-lg hover:from-primary-700 hover:to-blue-700 transition-colors"
        >
          🏠 返回首页
        </button>
      </div>

      <!-- 搜索建议 -->
      <div class="mt-12">
        <p class="text-gray-600 mb-4">或者尝试搜索您需要的内容：</p>
        <div class="relative max-w-md mx-auto">
          <input
            type="text"
            placeholder="搜索页面..."
            class="w-full px-4 py-3 pl-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <span class="absolute left-4 top-3.5 text-gray-400">🔍</span>
        </div>
      </div>

      <!-- 常用链接 -->
      <div class="mt-12 pt-8 border-t border-gray-200">
        <p class="text-gray-600 mb-4">常用页面：</p>
        <div class="flex flex-wrap justify-center gap-4">
          <router-link
            v-for="link in quickLinks"
            :key="link.to"
            :to="link.to"
            class="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors"
          >
            {{ link.label }}
          </router-link>
        </div>
      </div>

      <!-- 技术支持 -->
      <div class="mt-12 text-center text-sm text-gray-500">
        <p>需要帮助？请联系技术支持：</p>
        <p class="mt-1">
          📞 电话：400-123-4567 | ✉️ 邮箱：support@company.com
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const quickLinks = [
  { to: '/dashboard', label: '仪表盘' },
  { to: '/suppliers', label: '供应商管理' },
  { to: '/procurement', label: '采购管理' },
  { to: '/inventory', label: '库存管理' },
  { to: '/analytics', label: '报表分析' },
]

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/dashboard')
  }
}

const goHome = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
/* 404页面样式 */
</style>