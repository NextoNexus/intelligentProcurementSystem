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
            <p class="text-2xl font-bold mt-2">{{ userStats.total_users }}</p>
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
            <p class="text-2xl font-bold mt-2">{{ userStats.admin_count }}</p>
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
            <p class="text-2xl font-bold mt-2">{{ userStats.department_head_count }}</p>
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
            <p class="text-2xl font-bold mt-2">{{ userStats.active_users }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-purple-600">✅</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 第二行用户统计 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">员工数量</p>
            <p class="text-2xl font-bold mt-2">{{ userStats.employee_count }}</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-yellow-600">👤</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">最近7天新增</p>
            <p class="text-2xl font-bold mt-2">{{ userStats.recent_users_7d }}</p>
          </div>
          <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-indigo-600">📈</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 部门分布统计 -->
    <div class="bg-white rounded-xl shadow p-6 mb-8">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900">部门用户分布</h3>
        <span class="text-sm text-gray-500">共 {{ userStats.department_stats.length }} 个部门</span>
      </div>
      <div v-if="userStats.department_stats.length > 0">
        <div class="space-y-3">
          <div v-for="dept in userStats.department_stats" :key="dept.department" class="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
            <div class="flex items-center">
              <div class="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
              <span class="font-medium text-gray-800">{{ dept.department || '未分配部门' }}</span>
            </div>
            <div class="flex items-center">
              <span class="text-lg font-bold text-gray-900 mr-2">{{ dept.count }}</span>
              <span class="text-sm text-gray-500">人</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-8 text-gray-500">
        <p>暂无部门分布数据</p>
      </div>
    </div>

    <!-- 添加用户对话框 -->
    <div v-if="showAddDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-lg w-full max-w-2xl mx-4">
        <div class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">添加新用户</h2>
            <button @click="showAddDialog = false" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
          </div>
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">用户名 *</label>
                <input v-model="addUserForm.username" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">邮箱 *</label>
                <input v-model="addUserForm.email" type="email" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">登录密码 *</label>
                <input v-model="addUserForm.password" type="password" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">确认密码 *</label>
                <input type="password" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">真实姓名</label>
                <input v-model="addUserForm.full_name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">电话号码</label>
                <input v-model="addUserForm.phone" type="tel" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">部门</label>
                <input v-model="addUserForm.department" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm fontmedium text-gray-700 mb-1">职位</label>
                <input v-model="addUserForm.position" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">角色</label>
                <select v-model="addUserForm.role_ids" multiple class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
                  <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
                </select>
                <p class="text-xs text-gray-500 mt-1">按住Ctrl键可选择多个角色</p>
              </div>
            </div>
            <div class="flex items-center">
              <input v-model="addUserForm.is_active" type="checkbox" id="add-active" class="mr-2">
              <label for="add-active" class="text-sm text-gray-700">用户激活状态</label>
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-8">
            <button @click="showAddDialog = false" class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">取消</button>
            <button @click="handleAddUser" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">确定</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑用户对话框 -->
    <div v-if="showEditDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-lg w-full max-w-2xl mx-4">
        <div class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">编辑用户</h2>
            <button @click="showEditDialog = false" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
          </div>
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">用户名 *</label>
                <input v-model="editUserForm.username" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">邮箱 *</label>
                <input v-model="editUserForm.email" type="email" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">登录密码</label>
                <input v-model="editUserForm.password" type="password" placeholder="留空表示不修改" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
                <input type="password" placeholder="留空表示不修改" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">真实姓名</label>
                <input v-model="editUserForm.full_name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">电话号码</label>
                <input v-model="editUserForm.phone" type="tel" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">部门</label>
                <input v-model="editUserForm.department" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">职位</label>
                <input v-model="editUserForm.position" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">角色</label>
                <select v-model="editUserForm.role_ids" multiple class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
                  <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
                </select>
                <p class="text-xs text-gray-500 mt-1">按住Ctrl键可选择多个角色</p>
              </div>
            </div>
            <div class="flex items-center">
              <input v-model="editUserForm.is_active" type="checkbox" id="edit-active" class="mr-2">
              <label for="edit-active" class="text-sm text-gray-700">用户激活状态</label>
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-8">
            <button @click="showEditDialog = false" class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">取消</button>
            <button @click="handleUpdateUser" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">确定</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-lg w-full max-w-md mx-4">
        <div class="p-6">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4">
              <span class="text-2xl text-red-600">🗑️</span>
            </div>
            <h2 class="text-xl font-bold text-gray-900">确认删除</h2>
          </div>
          <p class="text-gray-600 mb-6">确定要删除用户 <strong>{{ userToDelete?.username }}</strong> 吗？此操作不可恢复。</p>
          <div class="flex justify-end space-x-3">
            <button @click="showDeleteDialog = false" class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">取消</button>
            <button @click="handleDeleteUser" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">确定删除</button>
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
      <button @click="openAddDialog" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        + 添加用户
      </button>
    </div>

    <!-- 用户表格 -->
    <div class="bg-white rounded-xl shadow overflow-x-auto mb-8">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider max-w-md">
              用户信息
            </th>
            <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              角色
            </th>
            <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs">
              部门
            </th>
            <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs">
              最后登录
            </th>
            <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              状态
            </th>
            <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading">
            <td colspan="6" class="px-2 py-4 text-center">
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
            <td class="px-2 py-4 whitespace-nowrap max-w-md">
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
            <td class="px-2 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs rounded-full" :class="getUserRoleClass(user)">
                {{ getUserRole(user) }}
              </span>
            </td>
            <td class="px-2 py-4 whitespace-nowrap text-sm text-gray-900 max-w-xs">
              {{ user.department || '-' }}
            </td>
            <td class="px-2 py-4 whitespace-nowrap text-sm text-gray-500 max-w-xs">
              {{ formatDate(user.last_login_at) }}
            </td>
            <td class="px-2 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs rounded-full" :class="getUserStatusClass(user)">
                {{ getUserStatus(user) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button @click="openEditDialog(user)" class="text-primary-600 hover:text-primary-900 mr-3">编辑</button>
              <button @click="openDeleteDialog(user)" class="text-red-600 hover:text-red-900">
                <span class="text-md">删除</span>
              </button>
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
const userStats = ref({
  total_users: 0,
  active_users: 0,
  inactive_users: 0,
  admin_count: 0,
  department_head_count: 0,
  employee_count: 0,
  recent_users_7d: 0,
  department_stats: [],
  last_updated: null,
  status: ''
})

// 对话框控制
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)

// 表单数据
const addUserForm = ref({
  username: '',
  email: '',
  password: '',
  full_name: '',
  phone: '',
  department: '',
  position: '',
  role_ids: [],
  is_active: true
})

const editUserForm = ref({
  id: null,
  username: '',
  email: '',
  password: '',
  full_name: '',
  phone: '',
  department: '',
  position: '',
  role_ids: [],
  is_active: true
})

const userToDelete = ref(null)

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

    // TODO: Implement role name to ID mapping for server-side filtering
    // Currently doing client-side filtering due to API expecting role_id (UUID)
    // Backend API expects role_id parameter, not role name
    const params = {
      search: searchQuery.value || undefined,
      is_active: selectedStatus.value !== 'all' ? (selectedStatus.value === 'active') : undefined
    }

    const response = await usersAPI.getUsers(params)
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

// 获取用户统计数据
const fetchUserStatistics = async () => {
  try {
    const response = await usersAPI.getUserStatistics()
    userStats.value = response
  } catch (err) {
    console.error('获取用户统计数据失败:', err)
    // 使用默认值
    userStats.value = {
      total_users: 0,
      active_users: 0,
      inactive_users: 0,
      admin_count: 0,
      department_head_count: 0,
      employee_count: 0,
      recent_users_7d: 0,
      department_stats: [],
      last_updated: null,
      status: ''
    }
  }
}

// 对话框操作函数
const openAddDialog = () => {
  // 重置表单
  addUserForm.value = {
    username: '',
    email: '',
    password: '',
    full_name: '',
    phone: '',
    department: '',
    position: '',
    role_ids: [],
    is_active: true
  }
  showAddDialog.value = true
}

const openEditDialog = (user) => {
  // 填充表单数据
  editUserForm.value = {
    id: user.id,
    username: user.username,
    email: user.email,
    password: '', // 密码留空，表示不修改
    full_name: user.full_name || '',
    phone: user.phone || '',
    department: user.department || '',
    position: user.position || '',
    role_ids: user.role_ids || [],
    is_active: user.is_active
  }
  showEditDialog.value = true
}

const openDeleteDialog = (user) => {
  userToDelete.value = user
  showDeleteDialog.value = true
}

const handleAddUser = async () => {
  try {
    // 简单验证
    if (!addUserForm.value.username || !addUserForm.value.email || !addUserForm.value.password) {
      alert('请填写必填字段：用户名、邮箱和密码')
      return
    }

    // 准备数据
    const userData = {
      username: addUserForm.value.username,
      email: addUserForm.value.email,
      password: addUserForm.value.password,
      full_name: addUserForm.value.full_name,
      phone: addUserForm.value.phone,
      department: addUserForm.value.department,
      position: addUserForm.value.position,
      role_ids: addUserForm.value.role_ids,
      is_active: addUserForm.value.is_active
    }

    await usersAPI.createUser(userData)

    // 刷新数据
    fetchUsers()
    fetchUserStatistics()

    // 关闭对话框
    showAddDialog.value = false

    alert('用户添加成功')
  } catch (err) {
    console.error('添加用户失败:', err)
    alert('添加用户失败：' + (err.response?.data?.detail || err.message))
  }
}

const handleUpdateUser = async () => {
  try {
    // 简单验证
    if (!editUserForm.value.username || !editUserForm.value.email) {
      alert('请填写必填字段：用户名和邮箱')
      return
    }

    // 准备数据
    const updateData = {
      username: editUserForm.value.username,
      email: editUserForm.value.email,
      full_name: editUserForm.value.full_name,
      phone: editUserForm.value.phone,
      department: editUserForm.value.department,
      position: editUserForm.value.position,
      role_ids: editUserForm.value.role_ids,
      is_active: editUserForm.value.is_active
    }

    // 如果有新密码，添加密码字段
    if (editUserForm.value.password) {
      updateData.password = editUserForm.value.password
    }

    await usersAPI.updateUser(editUserForm.value.id, updateData)

    // 刷新数据
    fetchUsers()
    fetchUserStatistics()

    // 关闭对话框
    showEditDialog.value = false

    alert('用户信息更新成功')
  } catch (err) {
    console.error('更新用户失败:', err)
    alert('更新用户失败：' + (err.response?.data?.detail || err.message))
  }
}

const handleDeleteUser = async () => {
  if (!userToDelete.value) return

  try {
    await usersAPI.deleteUser(userToDelete.value.id)

    // 刷新数据
    fetchUsers()
    fetchUserStatistics()

    // 关闭对话框
    showDeleteDialog.value = false
    userToDelete.value = null

    alert('用户删除成功')
  } catch (err) {
    console.error('删除用户失败:', err)
    alert('删除用户失败：' + (err.response?.data?.detail || err.message))
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
  fetchUserStatistics()
})
</script>