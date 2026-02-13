<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">用户管理</h1>
      <p class="text-gray-600 mt-2">管理系统用户、角色和权限</p>
    </div>

    <!-- 用户统计 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">总用户数</p>
            <p class="text-2xl font-bold mt-2">156</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-blue-600">👥</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">管理员</p>
            <p class="text-2xl font-bold mt-2">8</p>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-red-600">👑</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">部门领导</p>
            <p class="text-2xl font-bold mt-2">24</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-green-600">👔</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">活跃用户</p>
            <p class="text-2xl font-bold mt-2">142</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-purple-600">✅</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input
            type="text"
            placeholder="搜索用户..."
            v-model="searchQuery"
            @input="fetchUsers"
            class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <span class="absolute left-3 top-2.5 text-gray-400">🔍</span>
        </div>
        <select v-model="selectedRole" @change="fetchUsers" class="px-4 py-2 border border-gray-300 rounded-lg">
          <option value="all">所有角色</option>
          <option value="admin">管理员</option>
          <option value="department_head">部门领导</option>
          <option value="management">管理层</option>
          <option value="employee">员工</option>
        </select>
        <select v-model="selectedStatus" @change="fetchUsers" class="px-4 py-2 border border-gray-300 rounded-lg">
          <option value="all">所有状态</option>
          <option value="active">活跃</option>
          <option value="inactive">停用</option>
        </select>
      </div>
      <button class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        + 添加用户
      </button>
    </div>

    <!-- 用户表格 -->
    <div class="bg-white rounded-xl shadow overflow-hidden mb-8">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              用户信息
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              角色
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              部门
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              最后登录
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              状态
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading">
            <td colspan="6" class="px-6 py-4 text-center">
              <div class="flex justify-center items-center">
                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
                <span class="ml-2">加载中...</span>
              </div>
            </td>
          </tr>
          <tr v-else-if="error">
            <td colspan="6" class="px-6 py-4 text-center text-red-600">
              {{ error }}
            </td>
          </tr>
          <tr v-else-if="filteredUsers.length === 0">
            <td colspan="6" class="px-6 py-4 text-center text-gray-500">
              没有找到用户
            </td>
          </tr>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-gray-300 rounded-full mr-3 flex items-center justify-center">
                  <span class="text-gray-600 text-sm">{{ user.username ? user.username.charAt(0).toUpperCase() : '' }}</span>
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ user.full_name || user.username }}</div>
                  <div class="text-sm text-gray-500">{{ user.email }}</div>
                  <div v-if="user.employee_id" class="text-xs text-gray-400">{{ user.employee_id }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs rounded-full" :class="getUserRoleClass(user)">
                {{ getUserRole(user) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ user.department || '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(user.last_login_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs rounded-full" :class="getUserStatusClass(user)">
                {{ getUserStatus(user) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button class="text-primary-600 hover:text-primary-900 mr-3">编辑</button>
              <button class="text-gray-600 hover:text-gray-900">重置密码</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 角色管理 -->
    <div class="bg-white rounded-xl shadow p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold text-gray-900">角色与权限</h2>
        <button class="px-3 py-1 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm">
          + 添加角色
        </button>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="role in roles" :key="role.id" class="border border-gray-200 rounded-lg p-5">
          <div class="flex items-center justify-between mb-3">
            <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-gray-100">
              <span class="text-xl text-gray-600">
                {{ role.name === 'admin' ? '👑' : role.name === 'department_head' ? '👔' : role.name === 'management' ? '💼' : '👤' }}
              </span>
            </div>
            <span class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">{{ role.user_count || 0 }} 用户</span>
          </div>
          <h3 class="font-bold text-gray-900 mb-2">{{ role.name }}</h3>
          <p class="text-sm text-gray-600 mb-4">{{ role.description || '暂无描述' }}</p>
          <div class="space-y-2 mb-4">
            <div v-if="role.permissions && role.permissions.length > 0" class="flex flex-wrap gap-1">
              <span v-for="perm in role.permissions.slice(0, 3)" :key="perm" class="px-1.5 py-0.5 text-xs bg-blue-100 text-blue-800 rounded">
                {{ perm }}
              </span>
              <span v-if="role.permissions.length > 3" class="px-1.5 py-0.5 text-xs bg-gray-100 text-gray-600 rounded">
                +{{ role.permissions.length - 3 }}
              </span>
            </div>
            <div v-else class="text-xs text-gray-400">暂无权限</div>
          </div>
          <button class="w-full px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm">
            管理权限
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { usersAPI } from '@/services/api'

// 响应式数据
const users = ref([])
const roles = ref([])
const loading = ref(true)
const error = ref(null)

// 搜索和过滤条件
const searchQuery = ref('')
const selectedRole = ref('all')
const selectedStatus = ref('all')

// 计算属性：过滤后的用户列表
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    // 搜索过滤
    const searchMatch = !searchQuery.value ||
      user.username?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.full_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.email?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.employee_id?.toLowerCase().includes(searchQuery.value.toLowerCase())

    // 角色过滤
    const roleMatch = selectedRole.value === 'all' ||
      user.roles?.some(role => role === selectedRole.value)

    // 状态过滤
    const statusMatch = selectedStatus.value === 'all' ||
      (selectedStatus.value === 'active' && user.is_active) ||
      (selectedStatus.value === 'inactive' && !user.is_active)

    return searchMatch && roleMatch && statusMatch
  })
})

// 获取用户列表
const fetchUsers = async () => {
  try {
    loading.value = true
    const response = await usersAPI.getUsers({
      search: searchQuery.value || undefined,
      role: selectedRole.value !== 'all' ? selectedRole.value : undefined,
      is_active: selectedStatus.value !== 'all' ? (selectedStatus.value === 'active') : undefined
    })
    users.value = response
    error.value = null
  } catch (err) {
    console.error('获取用户列表失败:', err)
    error.value = '获取用户列表失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 获取角色列表
const fetchRoles = async () => {
  try {
    const response = await usersAPI.getSimpleRoles()
    roles.value = response
  } catch (err) {
    console.error('获取角色列表失败:', err)
  }
}

// 用户状态文本和样式
const getUserStatus = (user) => {
  return user.is_active ? '活跃' : '停用'
}

const getUserStatusClass = (user) => {
  return user.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
}

// 用户角色文本和样式
const getUserRole = (user) => {
  return user.roles?.[0] || '未分配'
}

const getUserRoleClass = (user) => {
  const role = getUserRole(user)
  switch (role) {
    case 'admin': return 'bg-red-100 text-red-800'
    case 'department_head': return 'bg-blue-100 text-blue-800'
    case 'management': return 'bg-purple-100 text-purple-800'
    case 'employee': return 'bg-gray-100 text-gray-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 初始化加载
onMounted(() => {
  fetchUsers()
  fetchRoles()
})
</script>