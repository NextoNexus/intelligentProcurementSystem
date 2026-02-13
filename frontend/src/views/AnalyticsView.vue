<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">报表分析</h1>
      <p class="text-gray-600 mt-2">采购数据分析和业务洞察</p>
    </div>

    <!-- 分析概览 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">采购总额</p>
            <p class="text-2xl font-bold mt-2">¥ 12.8M</p>
            <p class="text-sm text-green-600 mt-1">↑ 8.5% 同比</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-blue-600">📊</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">平均采购周期</p>
            <p class="text-2xl font-bold mt-2">18天</p>
            <p class="text-sm text-red-600 mt-1">↓ 2天 同比</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-green-600">⏱️</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">供应商数量</p>
            <p class="text-2xl font-bold mt-2">128</p>
            <p class="text-sm text-green-600 mt-1">↑ 12家 同比</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-yellow-600">🏢</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">成本节约</p>
            <p class="text-2xl font-bold mt-2">¥ 2.4M</p>
            <p class="text-sm text-green-600 mt-1">↑ 15% 同比</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-purple-600">💰</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- 月度采购趋势 -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">月度采购趋势</h2>
        <div class="h-64 flex items-end space-x-4 pt-8">
          <div v-for="month in monthlyTrend" :key="month.id" class="flex-1 flex flex-col items-center">
            <div
              class="w-12 bg-gradient-to-t from-primary-500 to-primary-300 rounded-t-lg"
              :style="{ height: month.height }"
            ></div>
            <p class="mt-2 text-sm text-gray-500">{{ month.month }}</p>
            <p class="text-xs font-medium">{{ month.value }}</p>
          </div>
        </div>
      </div>

      <!-- 供应商分布 -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">供应商分类分布</h2>
        <div class="h-64 flex items-center justify-center">
          <div class="relative w-48 h-48">
            <!-- 简单的饼图示意 -->
            <div class="absolute inset-0 rounded-full border-8 border-blue-500"></div>
            <div class="absolute inset-0 rounded-full border-8 border-green-500" style="clip-path: polygon(50% 50%, 50% 0%, 100% 0%, 100% 100%, 50% 100%);"></div>
            <div class="absolute inset-0 rounded-full border-8 border-yellow-500" style="clip-path: polygon(50% 50%, 100% 0%, 100% 100%, 0% 100%, 0% 50%);"></div>
            <div class="absolute inset-0 rounded-full border-8 border-purple-500" style="clip-path: polygon(50% 50%, 0% 100%, 0% 0%, 50% 0%);"></div>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4 mt-6">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-blue-500 rounded mr-2"></div>
            <span class="text-sm">网络设备</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 rounded mr-2"></div>
            <span class="text-sm">计算机设备</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-yellow-500 rounded mr-2"></div>
            <span class="text-sm">办公耗材</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-purple-500 rounded mr-2"></div>
            <span class="text-sm">其他</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门报告 -->
    <div class="bg-white rounded-xl shadow p-6">
      <h2 class="text-xl font-bold text-gray-900 mb-4">热门分析报告</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="report in popularReports" :key="report.id" class="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-3">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center" :class="report.bgColor">
              <span class="text-2xl">{{ report.icon }}</span>
            </div>
            <span class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">{{ report.type }}</span>
          </div>
          <h3 class="font-bold text-gray-900 mb-2">{{ report.title }}</h3>
          <p class="text-sm text-gray-600 mb-4">{{ report.description }}</p>
          <div class="flex items-center justify-between">
            <span class="text-xs text-gray-500">{{ report.date }}</span>
            <button class="text-primary-600 hover:text-primary-800 text-sm font-medium">查看报告</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分析工具 -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📈 自定义报表</h3>
        <p class="text-gray-600 mb-4">根据需求创建自定义分析报表</p>
        <button class="px-4 py-2 bg-white border border-blue-500 text-blue-600 rounded-lg hover:bg-blue-50">
          创建报表
        </button>
      </div>
      <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">🔍 数据对比</h3>
        <p class="text-gray-600 mb-4">对比不同时期、部门的采购数据</p>
        <button class="px-4 py-2 bg-white border border-green-500 text-green-600 rounded-lg hover:bg-green-50">
          数据对比
        </button>
      </div>
      <div class="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📤 导出数据</h3>
        <p class="text-gray-600 mb-4">导出分析数据用于外部处理</p>
        <button class="px-4 py-2 bg-white border border-purple-500 text-purple-600 rounded-lg hover:bg-purple-50">
          导出数据
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const monthlyTrend = ref([
  { id: 1, month: '9月', value: '¥ 1.2M', height: '40%' },
  { id: 2, month: '10月', value: '¥ 1.5M', height: '50%' },
  { id: 3, month: '11月', value: '¥ 1.8M', height: '60%' },
  { id: 4, month: '12月', value: '¥ 2.1M', height: '70%' },
  { id: 5, month: '1月', value: '¥ 1.9M', height: '65%' },
  { id: 6, month: '2月', value: '¥ 1.7M', height: '55%' },
])

const popularReports = ref([
  {
    id: 1,
    icon: '📊',
    bgColor: 'bg-blue-100',
    type: '月度报告',
    title: '2024年1月采购分析报告',
    description: '本月采购总额、供应商表现、成本节约分析',
    date: '2024-01-31'
  },
  {
    id: 2,
    icon: '🏢',
    bgColor: 'bg-green-100',
    type: '供应商评估',
    title: 'Top 10供应商绩效评估',
    description: '基于质量、价格、交付时间的供应商排名',
    date: '2024-01-28'
  },
  {
    id: 3,
    icon: '💰',
    bgColor: 'bg-yellow-100',
    type: '成本分析',
    title: '年度成本节约报告',
    description: '通过集中采购和谈判实现的成本节约',
    date: '2024-01-25'
  },
  {
    id: 4,
    icon: '📦',
    bgColor: 'bg-purple-100',
    type: '库存分析',
    title: '库存周转率分析',
    description: '各类物资库存周转效率和优化建议',
    date: '2024-01-20'
  },
  {
    id: 5,
    icon: '⏱️',
    bgColor: 'bg-red-100',
    type: '效率分析',
    title: '采购周期效率报告',
    description: '各环节采购周期分析和优化建议',
    date: '2024-01-18'
  },
  {
    id: 6,
    icon: '📈',
    bgColor: 'bg-indigo-100',
    type: '趋势预测',
    title: '2024年采购需求预测',
    description: '基于历史数据的采购需求趋势预测',
    date: '2024-01-15'
  },
])
</script>