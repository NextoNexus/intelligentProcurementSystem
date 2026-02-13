import axios from 'axios'
import router from '@/router'

// 创建axios实例
const api = axios.create({
  baseURL: '/api', // 使用Vite代理
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const { response } = error

    // 处理HTTP错误状态
    if (response) {
      switch (response.status) {
        case 401:
          // 未授权，跳转到登录页面
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user_info')
          router.push('/login')
          break
        case 403:
          // 权限不足
          console.error('权限不足，无法访问该资源')
          break
        case 404:
          // 资源不存在
          console.error('请求的资源不存在')
          break
        case 500:
          // 服务器错误
          console.error('服务器内部错误')
          break
        default:
          console.error(`请求错误: ${response.status}`)
      }
    } else {
      // 网络错误或请求超时
      console.error('网络错误，请检查网络连接')
    }

    return Promise.reject(error)
  }
)

// API端点
export const authAPI = {
  // 用户注册
  register: (userData) => api.post('/auth/register', userData),

  // 用户登录
  login: (credentials) => api.post('/auth/login', credentials),

  // 刷新token
  refreshToken: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),

  // 获取当前用户信息
  getCurrentUser: () => api.get('/auth/me'),
}

export const usersAPI = {
  // 获取用户列表（管理员）
  getUsers: (params) => api.get('/users/', { params }),

  // 获取用户详情
  getUser: (id) => api.get(`/users/${id}`),

  // 创建用户
  createUser: (data) => api.post('/users', data),

  // 更新用户
  updateUser: (id, data) => api.put(`/users/${id}`, data),

  // 删除用户
  deleteUser: (id) => api.delete(`/users/${id}`),

  // 更新用户角色
  updateUserRoles: (id, roleIds) => api.put(`/users/${id}/roles`, roleIds),

  // 重置用户密码
  resetUserPassword: (id, newPassword) => api.put(`/users/${id}/password`, { new_password: newPassword }),

  // 获取简化用户列表
  getSimpleUsers: () => api.get('/users/simple/'),

  // 角色管理
  getRoles: (params) => api.get('/users/roles/', { params }),
  getRole: (id) => api.get(`/users/roles/${id}`),
  createRole: (data) => api.post('/users/roles/', data),
  updateRole: (id, data) => api.put(`/users/roles/${id}`, data),
  deleteRole: (id) => api.delete(`/users/roles/${id}`),
  getSimpleRoles: () => api.get('/users/roles/simple/'),

  // 权限管理
  getPermissions: (params) => api.get('/users/permissions/', { params }),
  getPermission: (id) => api.get(`/users/permissions/${id}`),
  createPermission: (data) => api.post('/users/permissions/', data),
  updatePermission: (id, data) => api.put(`/users/permissions/${id}`, data),
  deletePermission: (id) => api.delete(`/users/permissions/${id}`),
  getSimplePermissions: (params) => api.get('/users/permissions/simple/', { params }),
}

export const suppliersAPI = {
  // 获取供应商列表
  getSuppliers: (params) => api.get('/suppliers', { params }),

  // 获取供应商详情
  getSupplier: (id) => api.get(`/suppliers/${id}`),

  // 创建供应商
  createSupplier: (data) => api.post('/suppliers', data),

  // 更新供应商
  updateSupplier: (id, data) => api.put(`/suppliers/${id}`, data),

  // 删除供应商
  deleteSupplier: (id) => api.delete(`/suppliers/${id}`),

  // 供应商产品管理
  getSupplierProducts: (supplierId, params) => api.get(`/suppliers/${supplierId}/products`, { params }),
  createSupplierProduct: (supplierId, data) => api.post(`/suppliers/${supplierId}/products`, data),
  getSupplierProduct: (productId) => api.get(`/suppliers/products/${productId}`),
  updateSupplierProduct: (productId, data) => api.put(`/suppliers/products/${productId}`, data),
  deleteSupplierProduct: (productId) => api.delete(`/suppliers/products/${productId}`),

  // 供应商评估管理
  getSupplierEvaluations: (supplierId, params) => api.get(`/suppliers/${supplierId}/evaluations`, { params }),
  createSupplierEvaluation: (supplierId, data) => api.post(`/suppliers/${supplierId}/evaluations`, data),
  getSupplierEvaluation: (evaluationId) => api.get(`/suppliers/evaluations/${evaluationId}`),
  updateSupplierEvaluation: (evaluationId, data) => api.put(`/suppliers/evaluations/${evaluationId}`, data),
  deleteSupplierEvaluation: (evaluationId) => api.delete(`/suppliers/evaluations/${evaluationId}`),

  // 简化供应商列表
  getSimpleSuppliers: (params) => api.get('/suppliers/simple/', { params }),
}

export const procurementAPI = {
  // 获取采购需求列表
  getProcurementRequests: (params) => api.get('/procurement/requests', { params }),

  // 创建采购需求
  createProcurementRequest: (data) => api.post('/procurement/requests', data),

  // 获取采购需求详情
  getProcurementRequest: (id) => api.get(`/procurement/requests/${id}`),

  // 更新采购需求状态
  updateProcurementRequest: (id, data) => api.put(`/procurement/requests/${id}`, data),
}

export const inventoryAPI = {
  // 获取库存列表
  getInventory: (params) => api.get('/inventory', { params }),

  // 获取库存项详情
  getInventoryItem: (id) => api.get(`/inventory/${id}`),

  // 入库操作
  stockIn: (data) => api.post('/inventory/stock-in', data),

  // 出库操作
  stockOut: (data) => api.post('/inventory/stock-out', data),
}

export const aiAPI = {
  // AI聊天
  chat: (message) => api.post('/ai/chat', { message }),

  // 数据库查询
  query: (query) => api.post('/ai/query', { query }),
}

// 工具函数
export const authUtils = {
  // 保存token
  saveTokens: (accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
  },

  // 获取token
  getTokens: () => ({
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
  }),

  // 清除token
  clearTokens: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_info')
  },

  // 检查是否已登录
  isLoggedIn: () => {
    return !!localStorage.getItem('access_token')
  },

  // 保存用户信息
  saveUserInfo: (userInfo) => {
    localStorage.setItem('user_info', JSON.stringify(userInfo))
  },

  // 获取用户信息
  getUserInfo: () => {
    const userInfo = localStorage.getItem('user_info')
    return userInfo ? JSON.parse(userInfo) : null
  },
}

export default api