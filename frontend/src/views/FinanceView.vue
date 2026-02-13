<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">财务管理</h1>
      <p class="text-gray-600 mt-2">管理采购成本、发票和付款流程</p>
    </div>

    <!-- 财务概览 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">本月采购支出</p>
            <p class="text-2xl font-bold mt-2">¥ 1,245,000</p>
            <p class="text-sm text-green-600 mt-1">↑ 12% 同比</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-blue-600">💰</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">待处理发票</p>
            <p class="text-2xl font-bold mt-2">18</p>
            <p class="text-sm text-yellow-600 mt-1">¥ 450,000</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-yellow-600">📄</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">已付款项</p>
            <p class="text-2xl font-bold mt-2">¥ 3,780,000</p>
            <p class="text-sm text-gray-500 mt-1">本季度</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-green-600">✅</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">预算使用率</p>
            <p class="text-2xl font-bold mt-2">78%</p>
            <div class="mt-2 w-full bg-gray-200 rounded-full h-2">
              <div class="bg-primary-600 h-2 rounded-full" style="width: 78%"></div>
            </div>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-purple-600">📊</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 发票管理 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- 待处理发票 -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">待处理发票</h2>
        <div class="space-y-4">
          <div v-for="invoice in pendingInvoices" :key="invoice.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h4 class="font-medium text-gray-900">{{ invoice.supplier }}</h4>
              <p class="text-sm text-gray-500">{{ invoice.invoiceNo }} • {{ invoice.date }}</p>
            </div>
            <div class="text-right">
              <p class="font-bold text-gray-900">{{ invoice.amount }}</p>
              <span class="text-xs px-2 py-1 rounded-full" :class="invoice.statusClass">{{ invoice.status }}</span>
            </div>
          </div>
        </div>
        <button class="w-full mt-4 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
          查看所有发票
        </button>
      </div>

      <!-- 付款记录 -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">最近付款记录</h2>
        <div class="space-y-4">
          <div v-for="payment in recentPayments" :key="payment.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-gray-200 rounded-lg mr-4"></div>
              <div>
                <h4 class="font-medium text-gray-900">{{ payment.supplier }}</h4>
                <p class="text-sm text-gray-500">{{ payment.date }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="font-bold text-green-600">{{ payment.amount }}</p>
              <p class="text-sm text-gray-500">{{ payment.method }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 财务操作 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📄 发票登记</h3>
        <p class="text-gray-600 mb-4">登记供应商发票，启动付款流程</p>
        <button class="px-4 py-2 bg-white border border-blue-500 text-blue-600 rounded-lg hover:bg-blue-50">
          登记发票
        </button>
      </div>
      <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">💳 付款处理</h3>
        <p class="text-gray-600 mb-4">处理供应商付款，记录付款凭证</p>
        <button class="px-4 py-2 bg-white border border-green-500 text-green-600 rounded-lg hover:bg-green-50">
          发起付款
        </button>
      </div>
      <div class="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📈 成本分析</h3>
        <p class="text-gray-600 mb-4">分析采购成本，优化预算分配</p>
        <button class="px-4 py-2 bg-white border border-purple-500 text-purple-600 rounded-lg hover:bg-purple-50">
          成本分析
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const pendingInvoices = ref([
  {
    id: 1,
    supplier: '华为技术有限公司',
    invoiceNo: 'INV-2024-001',
    date: '2024-01-15',
    amount: '¥ 450,000',
    status: '待审核',
    statusClass: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 2,
    supplier: '联想集团',
    invoiceNo: 'INV-2024-002',
    date: '2024-01-14',
    amount: '¥ 320,000',
    status: '待付款',
    statusClass: 'bg-blue-100 text-blue-800'
  },
  {
    id: 3,
    supplier: '格力电器',
    invoiceNo: 'INV-2024-003',
    date: '2024-01-13',
    amount: '¥ 150,000',
    status: '待审核',
    statusClass: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 4,
    supplier: '海尔集团',
    invoiceNo: 'INV-2024-004',
    date: '2024-01-12',
    amount: '¥ 280,000',
    status: '待付款',
    statusClass: 'bg-blue-100 text-blue-800'
  },
])

const recentPayments = ref([
  {
    id: 1,
    supplier: '中兴通讯',
    date: '2024-01-10',
    amount: '¥ 890,000',
    method: '银行转账'
  },
  {
    id: 2,
    supplier: '小米科技',
    date: '2024-01-09',
    amount: '¥ 540,000',
    method: '银行转账'
  },
  {
    id: 3,
    supplier: '比亚迪',
    date: '2024-01-08',
    amount: '¥ 1,200,000',
    method: '电汇'
  },
  {
    id: 4,
    supplier: '京东方',
    date: '2024-01-07',
    amount: '¥ 670,000',
    method: '银行转账'
  },
])
</script>