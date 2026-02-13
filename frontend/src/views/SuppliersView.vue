<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">供应商管理</h1>
      <p class="text-gray-600 mt-2">管理供应商信息、评估和合作关系</p>
    </div>

    <!-- 操作栏 -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input
            type="text"
            placeholder="搜索供应商..."
            v-model="searchQuery"
            @input="fetchSuppliers"
            class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <span class="absolute left-3 top-2.5 text-gray-400">🔍</span>
        </div>
        <select v-model="selectedStatus" @change="fetchSuppliers" class="px-4 py-2 border border-gray-300 rounded-lg">
          <option value="all">所有状态</option>
          <option value="active">活跃</option>
          <option value="inactive">不活跃</option>
          <option value="suspended">暂停</option>
          <option value="blacklisted">黑名单</option>
        </select>
      </div>
      <button class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
        + 添加供应商
      </button>
    </div>

    <!-- 供应商表格 -->
    <div class="bg-white rounded-xl shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              供应商名称
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              联系人
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              产品类别
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              评分
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
          <tr v-else-if="filteredSuppliers.length === 0">
            <td colspan="6" class="px-6 py-4 text-center text-gray-500">
              没有找到供应商
            </td>
          </tr>
          <tr v-for="supplier in filteredSuppliers" :key="supplier.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-gray-200 rounded-lg mr-3 flex items-center justify-center">
                  <span class="text-gray-600 text-sm">{{ supplier.name ? supplier.name.charAt(0).toUpperCase() : '' }}</span>
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ supplier.name }}</div>
                  <div class="text-sm text-gray-500">{{ supplier.code }}</div>
                  <div v-if="supplier.contact_email" class="text-xs text-gray-400">{{ supplier.contact_email }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ supplier.contact_person || '-' }}</div>
              <div class="text-sm text-gray-500">{{ supplier.contact_phone || '-' }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                {{ getSupplierType(supplier) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="text-yellow-400 mr-1">
                  <span v-for="i in 5" :key="i">
                    {{ i <= Math.floor(supplier.overall_rating) ? '★' : (i === Math.ceil(supplier.overall_rating) && supplier.overall_rating % 1 >= 0.5 ? '½' : '☆') }}
                  </span>
                </div>
                <span class="text-sm text-gray-600">{{ formatRating(supplier.overall_rating) }}/5</span>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs rounded-full" :class="getSupplierStatusClass(supplier)">
                {{ getSupplierStatus(supplier) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button class="text-primary-600 hover:text-primary-900 mr-3">查看</button>
              <button class="text-gray-600 hover:text-gray-900">编辑</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="flex items-center justify-between mt-6">
      <div class="text-sm text-gray-700">
        显示 <span class="font-medium">1</span> 到 <span class="font-medium">5</span> 条，共 <span class="font-medium">128</span> 条
      </div>
      <div class="flex space-x-2">
        <button class="px-3 py-2 border border-gray-300 rounded-lg text-gray-700">上一页</button>
        <button class="px-3 py-2 bg-primary-600 text-white rounded-lg">1</button>
        <button class="px-3 py-2 border border-gray-300 rounded-lg text-gray-700">2</button>
        <button class="px-3 py-2 border border-gray-300 rounded-lg text-gray-700">3</button>
        <button class="px-3 py-2 border border-gray-300 rounded-lg text-gray-700">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { suppliersAPI } from '@/services/api'

// 响应式数据
const suppliers = ref([])
const loading = ref(true)
const error = ref(null)

// 搜索和过滤条件
const searchQuery = ref('')
const selectedStatus = ref('all')

// 计算属性：过滤后的供应商列表
const filteredSuppliers = computed(() => {
  return suppliers.value.filter(supplier => {
    // 搜索过滤
    const searchMatch = !searchQuery.value ||
      supplier.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      supplier.code?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      supplier.contact_person?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      supplier.company_name?.toLowerCase().includes(searchQuery.value.toLowerCase())

    // 状态过滤
    const statusMatch = selectedStatus.value === 'all' ||
      supplier.status === selectedStatus.value

    return searchMatch && statusMatch
  })
})

// 获取供应商列表
const fetchSuppliers = async () => {
  try {
    loading.value = true
    const response = await suppliersAPI.getSuppliers({
      search: searchQuery.value || undefined,
      status: selectedStatus.value !== 'all' ? selectedStatus.value : undefined
    })
    suppliers.value = response
    error.value = null
  } catch (err) {
    console.error('获取供应商列表失败:', err)
    error.value = '获取供应商列表失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 供应商状态文本和样式
const getSupplierStatus = (supplier) => {
  const statusMap = {
    'active': '活跃',
    'inactive': '不活跃',
    'suspended': '暂停',
    'blacklisted': '黑名单'
  }
  return statusMap[supplier.status] || supplier.status
}

const getSupplierStatusClass = (supplier) => {
  const statusClassMap = {
    'active': 'bg-green-100 text-green-800',
    'inactive': 'bg-gray-100 text-gray-800',
    'suspended': 'bg-yellow-100 text-yellow-800',
    'blacklisted': 'bg-red-100 text-red-800'
  }
  return statusClassMap[supplier.status] || 'bg-gray-100 text-gray-800'
}

// 供应商类型文本
const getSupplierType = (supplier) => {
  const typeMap = {
    'general': '普通',
    'strategic': '战略',
    'key': '关键'
  }
  return typeMap[supplier.type] || supplier.type
}

// 格式化评分显示
const formatRating = (rating) => {
  return rating ? rating.toFixed(1) : '0.0'
}

// 初始化加载
onMounted(() => {
  fetchSuppliers()
})
</script>