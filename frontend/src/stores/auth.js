import { defineStore } from 'pinia'
import { authAPI, authUtils } from '@/services/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  getters: {
    // 用户角色
    userRoles: (state) => state.user?.roles || [],
    // 用户权限
    userPermissions: (state) => state.user?.permissions || [],
    // 用户基本信息
    userInfo: (state) => ({
      id: state.user?.id,
      username: state.user?.username,
      email: state.user?.email,
      fullName: state.user?.full_name,
      department: state.user?.department,
      position: state.user?.position
    }),
    // 检查是否具有特定角色
    hasRole: (state) => (role) => state.user?.roles?.includes(role) || false,
    // 检查是否具有特定权限
    hasPermission: (state) => (permission) => state.user?.permissions?.includes(permission) || false
  },

  actions: {
    // 初始化store（从localStorage恢复状态）
    initialize() {
      const tokens = authUtils.getTokens()
      const userInfo = authUtils.getUserInfo()

      if (tokens.accessToken && userInfo) {
        this.accessToken = tokens.accessToken
        this.refreshToken = tokens.refreshToken
        this.user = userInfo
        this.isAuthenticated = true
      }
    },

    // 用户注册
    async register(userData) {
      this.loading = true
      this.error = null

      try {
        const response = await authAPI.register(userData)
        this.user = response
        // 注册成功后自动登录
        await this.login({
          username: userData.username,
          password: userData.password
        })
        return { success: true, data: response }
      } catch (error) {
        this.error = error.response?.data?.detail || '注册失败'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    // 用户登录
    async login(credentials) {
      this.loading = true
      this.error = null

      try {
        const response = await authAPI.login(credentials)

        // 保存token
        this.accessToken = response.access_token
        this.refreshToken = response.refresh_token
        authUtils.saveTokens(response.access_token, response.refresh_token)

        // 获取用户信息
        const userInfo = await authAPI.getCurrentUser()
        this.user = userInfo
        this.isAuthenticated = true
        authUtils.saveUserInfo(userInfo)

        // 跳转到仪表盘
        router.push('/dashboard')

        return { success: true, data: userInfo }
      } catch (error) {
        this.error = error.response?.data?.detail || '登录失败'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    // 刷新token
    async refreshAccessToken() {
      if (!this.refreshToken) {
        this.logout()
        return false
      }

      try {
        const response = await authAPI.refreshToken(this.refreshToken)
        this.accessToken = response.access_token
        this.refreshToken = response.refresh_token
        authUtils.saveTokens(response.access_token, response.refresh_token)
        return true
      } catch (error) {
        console.error('刷新token失败:', error)
        this.logout()
        return false
      }
    },

    // 获取当前用户信息
    async fetchCurrentUser() {
      try {
        const userInfo = await authAPI.getCurrentUser()
        this.user = userInfo
        authUtils.saveUserInfo(userInfo)
        return userInfo
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return null
      }
    },

    // 用户登出
    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false
      authUtils.clearTokens()

      // 跳转到登录页面
      router.push('/login')
    },

    // 更新用户信息
    async updateUserInfo(userData) {
      try {
        // 这里应该调用更新用户信息的API
        // const response = await authAPI.updateUser(userData)
        this.user = { ...this.user, ...userData }
        authUtils.saveUserInfo(this.user)
        return { success: true, data: this.user }
      } catch (error) {
        console.error('更新用户信息失败:', error)
        return { success: false, error }
      }
    },

    // 检查token是否有效（简单检查）
    checkAuth() {
      if (!this.accessToken) {
        return false
      }

      // 这里可以添加更复杂的token验证逻辑
      // 例如检查token是否过期
      return true
    }
  },

  // 持久化存储
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'auth',
        storage: localStorage,
        paths: ['user', 'accessToken', 'refreshToken', 'isAuthenticated']
      }
    ]
  }
})