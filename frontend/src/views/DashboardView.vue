<template>
  <div>
    <!-- 页面标题 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">仪表盘</h1>
      <p class="text-gray-600 mt-2">欢迎使用智能物资采购管理系统</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">供应商总数</p>
            <p class="text-2xl font-bold mt-2">128</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-blue-600">🏢</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">待处理采购</p>
            <p class="text-2xl font-bold mt-2">24</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-green-600">📦</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">库存预警</p>
            <p class="text-2xl font-bold mt-2">8</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-yellow-600">⚠️</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">本月采购金额</p>
            <p class="text-2xl font-bold mt-2">¥ 1,245,000</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-purple-600">💰</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速操作 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- 最近活动 -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">最近活动</h2>
        <div class="space-y-4">
          <div v-for="activity in activities" :key="activity.id" class="flex items-start space-x-3">
            <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
              <span class="text-lg">{{ activity.icon }}</span>
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
              <p class="text-xs text-gray-500 mt-1">{{ activity.description }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ activity.time }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 待办事项 -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">待办事项</h2>
        <div class="space-y-3">
          <div v-for="task in tasks" :key="task.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div class="flex items-center space-x-3">
              <input type="checkbox" class="rounded text-primary-600" />
              <div>
                <p class="text-sm font-medium text-gray-900">{{ task.title }}</p>
                <p class="text-xs text-gray-500">{{ task.dueDate }}</p>
              </div>
            </div>
            <span class="px-2 py-1 text-xs rounded-full" :class="task.priorityClass">{{ task.priority }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activities = ref([
  { id: 1, icon: '📋', title: '新采购申请', description: '张三提交了办公用品采购申请', time: '10分钟前' },
  { id: 2, icon: '✅', title: '审批通过', description: '李四批准了服务器采购订单', time: '1小时前' },
  { id: 3, icon: '📦', title: '到货通知', description: '联想供应商发货了20台笔记本', time: '3小时前' },
  { id: 4, icon: '💰', title: '付款完成', description: '完成对华为技术的货款支付', time: '昨天' },
  { id: 5, icon: '📊', title: '月度报告', description: '系统自动生成10月采购分析报告', time: '2天前' },
])

const tasks = ref([
  { id: 1, title: '审核采购申请 #PR-2024-0012', dueDate: '今天', priority: '高', priorityClass: 'bg-red-100 text-red-800' },
  { id: 2, title: '联系供应商确认交货时间', dueDate: '明天', priority: '中', priorityClass: 'bg-yellow-100 text-yellow-800' },
  { id: 3, title: '更新库存分类信息', dueDate: '本周', priority: '低', priorityClass: 'bg-green-100 text-green-800' },
  { id: 4, title: '准备季度采购预算', dueDate: '下周一', priority: '高', priorityClass: 'bg-red-100 text-red-800' },
])
</script>