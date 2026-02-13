<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- 登录卡片 -->
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <!-- Logo -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-gradient-to-r from-primary-600 to-blue-600 rounded-2xl mx-auto mb-4 flex items-center justify-center">
            <span class="text-3xl text-white">📦</span>
          </div>
          <h1 class="text-2xl font-bold text-gray-900">智能采购系统</h1>
          <p class="text-gray-600 mt-2">企业物资采购管理平台</p>
        </div>

        <!-- 选项卡切换 -->
        <div class="flex mb-8 border-b border-gray-200">
          <button
            @click="activeTab = 'login'"
            class="flex-1 py-3 text-center font-medium transition-colors"
            :class="activeTab === 'login' ? 'text-primary-600 border-b-2 border-primary-600' : 'text-gray-500 hover:text-gray-700'"
          >
            登录账户
          </button>
          <button
            @click="activeTab = 'register'"
            class="flex-1 py-3 text-center font-medium transition-colors"
            :class="activeTab === 'register' ? 'text-primary-600 border-b-2 border-primary-600' : 'text-gray-500 hover:text-gray-700'"
          >
            注册账户
          </button>
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ error }}</p>
        </div>

        <!-- 登录表单 -->
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="login-username" class="block text-sm font-medium text-gray-700 mb-2">
              用户名或邮箱
            </label>
            <input
              id="login-username"
              v-model="loginForm.username"
              type="text"
              required
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请输入用户名或邮箱"
            />
          </div>

          <div>
            <label for="login-password" class="block text-sm font-medium text-gray-700 mb-2">
              密码
            </label>
            <input
              id="login-password"
              v-model="loginForm.password"
              type="password"
              required
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请输入密码"
            />
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                v-model="loginForm.rememberMe"
                type="checkbox"
                :disabled="loading"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:bg-gray-100"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                记住我
              </label>
            </div>
            <a href="#" class="text-sm text-primary-600 hover:text-primary-500">
              忘记密码？
            </a>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-gradient-to-r from-primary-600 to-blue-600 text-white font-medium rounded-lg hover:from-primary-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">登录中...</span>
            <span v-else>登录系统</span>
          </button>
        </form>

        <!-- 注册表单 -->
        <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="space-y-6">
          <div>
            <label for="register-username" class="block text-sm font-medium text-gray-700 mb-2">
              用户名
            </label>
            <input
              id="register-username"
              v-model="registerForm.username"
              type="text"
              required
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请输入用户名"
            />
          </div>

          <div>
            <label for="register-email" class="block text-sm font-medium text-gray-700 mb-2">
              邮箱
            </label>
            <input
              id="register-email"
              v-model="registerForm.email"
              type="email"
              required
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请输入邮箱地址"
            />
          </div>

          <div>
            <label for="register-fullname" class="block text-sm font-medium text-gray-700 mb-2">
              姓名
            </label>
            <input
              id="register-fullname"
              v-model="registerForm.full_name"
              type="text"
              required
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请输入您的真实姓名"
            />
          </div>

          <div>
            <label for="register-password" class="block text-sm font-medium text-gray-700 mb-2">
              密码
            </label>
            <input
              id="register-password"
              v-model="registerForm.password"
              type="password"
              required
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请输入密码"
            />
          </div>

          <div>
            <label for="register-confirm-password" class="block text-sm font-medium text-gray-700 mb-2">
              确认密码
            </label>
            <input
              id="register-confirm-password"
              v-model="registerForm.confirmPassword"
              type="password"
              required
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请再次输入密码"
            />
          </div>

          <div>
            <label for="register-department" class="block text-sm font-medium text-gray-700 mb-2">
              部门（可选）
            </label>
            <input
              id="register-department"
              v-model="registerForm.department"
              type="text"
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请输入所在部门"
            />
          </div>

          <div>
            <label for="register-position" class="block text-sm font-medium text-gray-700 mb-2">
              职位（可选）
            </label>
            <input
              id="register-position"
              v-model="registerForm.position"
              type="text"
              :disabled="loading"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="请输入职位"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-gradient-to-r from-primary-600 to-blue-600 text-white font-medium rounded-lg hover:from-primary-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">注册中...</span>
            <span v-else>注册账户</span>
          </button>
        </form>

        <!-- 其他登录方式（仅登录时显示） -->
        <div v-if="activeTab === 'login'" class="mt-8">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">其他登录方式</span>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-2 gap-3">
            <button type="button" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
              <span class="mr-2">📱</span> 手机验证码
            </button>
            <button type="button" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
              <span class="mr-2">🖥️</span> SSO登录
            </button>
          </div>
        </div>

        <!-- 切换提示 -->
        <p class="mt-8 text-center text-sm text-gray-600">
          <template v-if="activeTab === 'login'">
            还没有账户？
            <button @click="activeTab = 'register'" class="font-medium text-primary-600 hover:text-primary-500">
              立即注册
            </button>
          </template>
          <template v-else>
            已有账户？
            <button @click="activeTab = 'login'" class="font-medium text-primary-600 hover:text-primary-500">
              立即登录
            </button>
          </template>
        </p>
      </div>

      <!-- 底部信息 -->
      <div class="mt-8 text-center">
        <p class="text-sm text-gray-500">
          © 2024 企业智能物资采购管理系统
        </p>
        <p class="text-xs text-gray-400 mt-2">
          版本 v0.1.0 • 技术支持：信息技术部
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const activeTab = ref('login')
const loading = computed(() => authStore.loading)
const error = computed(() => authStore.error)

const loginForm = ref({
  username: '',
  password: '',
  rememberMe: false
})

const registerForm = ref({
  username: '',
  email: '',
  full_name: '',
  password: '',
  confirmPassword: '',
  department: '',
  position: ''
})

const handleLogin = async () => {
  // 清除之前的错误
  authStore.error = null

  const credentials = {
    username: loginForm.value.username,
    password: loginForm.value.password
  }

  const result = await authStore.login(credentials)
  if (!result.success) {
    // 错误信息已通过store设置
    console.error('登录失败:', result.error)
  }
}

const handleRegister = async () => {
  // 验证密码确认
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    authStore.error = '两次输入的密码不一致'
    return
  }

  // 清除之前的错误
  authStore.error = null

  const userData = {
    username: registerForm.value.username,
    email: registerForm.value.email,
    full_name: registerForm.value.full_name,
    password: registerForm.value.password,
    department: registerForm.value.department || null,
    position: registerForm.value.position || null
  }

  const result = await authStore.register(userData)
  if (!result.success) {
    // 错误信息已通过store设置
    console.error('注册失败:', result.error)
  }
}
</script>

<style scoped>
/* 登录页面样式 */
</style>