<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">采购管理</h1>
      <p class="text-gray-600 mt-2">管理采购需求、审批流程和订单跟踪</p>
    </div>

    <!-- 标签页 -->
    <div class="border-b border-gray-200 mb-6">
      <nav class="-mb-px flex space-x-8">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="py-3 px-1 border-b-2 font-medium text-sm"
          :class="activeTab === tab.id
            ? 'border-primary-500 text-primary-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
        >
          {{ tab.label }} <span class="ml-2 px-2 py-1 text-xs rounded-full bg-gray-100">{{ tab.count }}</span>
        </button>
      </nav>
    </div>

    <!-- 采购需求列表 -->
    <div class="space-y-4">
      <div v-for="request in procurementRequests" :key="request.id" class="bg-white rounded-xl shadow p-6">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div class="flex-1">
            <div class="flex items-start justify-between">
              <div>
                <h3 class="text-lg font-medium text-gray-900">{{ request.title }}</h3>
                <p class="text-gray-600 mt-1">{{ request.description }}</p>
              </div>
              <span class="px-3 py-1 text-sm rounded-full" :class="request.statusClass">
                {{ request.status }}
              </span>
            </div>
            <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p class="text-sm text-gray-500">申请人</p>
                <p class="font-medium">{{ request.requester }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">部门</p>
                <p class="font-medium">{{ request.department }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">预算</p>
                <p class="font-medium">{{ request.budget }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">提交时间</p>
                <p class="font-medium">{{ request.submittedDate }}</p>
              </div>
            </div>
          </div>
          <div class="flex flex-col sm:flex-row gap-3">
            <button class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
              查看详情
            </button>
            <button v-if="request.status === '待审批'" class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
              审批
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速操作卡片 -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-gradient-to-r from-primary-50 to-blue-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📋 提交采购需求</h3>
        <p class="text-gray-600 mb-4">提交新的采购需求，开始采购流程</p>
        <button class="px-4 py-2 bg-white border border-primary-500 text-primary-600 rounded-lg hover:bg-primary-50">
          新建需求
        </button>
      </div>
      <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📊 采购统计</h3>
        <p class="text-gray-600 mb-4">查看采购数据分析，优化采购策略</p>
        <button class="px-4 py-2 bg-white border border-green-500 text-green-600 rounded-lg hover:bg-green-50">
          查看统计
        </button>
      </div>
      <div class="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📦 订单跟踪</h3>
        <p class="text-gray-600 mb-4">跟踪已下订单的状态和物流信息</p>
        <button class="px-4 py-2 bg-white border border-purple-500 text-purple-600 rounded-lg hover:bg-purple-50">
          查看订单
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('pending')
const tabs = ref([
  { id: 'pending', label: '待审批', count: 8 },
  { id: 'approved', label: '已批准', count: 12 },
  { id: 'rejected', label: '已拒绝', count: 3 },
  { id: 'completed', label: '已完成', count: 24 },
])

const procurementRequests = ref([
  {
    id: 1,
    title: '办公电脑设备采购',
    description: '采购50台笔记本电脑用于新员工办公',
    requester: '张三',
    department: '信息技术部',
    budget: '¥ 450,000',
    submittedDate: '2024-01-15',
    status: '待审批',
    statusClass: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 2,
    title: '服务器设备升级',
    description: '采购3台高性能服务器用于数据中心扩容',
    requester: '李四',
    department: '运维部',
    budget: '¥ 1,200,000',
    submittedDate: '2024-01-14',
    status: '已批准',
    statusClass: 'bg-green-100 text-green-800'
  },
  {
    id: 3,
    title: '办公室家具采购',
    description: '采购办公桌椅、文件柜等家具',
    requester: '王五',
    department: '行政部',
    budget: '¥ 150,000',
    submittedDate: '2024-01-13',
    status: '待审批',
    statusClass: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 4,
    title: '软件开发工具',
    description: '采购开发工具软件和许可证',
    requester: '赵六',
    department: '研发部',
    budget: '¥ 80,000',
    submittedDate: '2024-01-12',
    status: '已完成',
    statusClass: 'bg-blue-100 text-blue-800'
  },
])
</script>