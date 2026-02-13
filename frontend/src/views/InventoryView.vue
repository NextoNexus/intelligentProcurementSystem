<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">库存管理</h1>
      <p class="text-gray-600 mt-2">监控库存水平，管理入库出库操作</p>
    </div>

    <!-- 库存概览 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">总库存价值</p>
            <p class="text-2xl font-bold mt-2">¥ 8,245,000</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-blue-600">💰</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">库存种类</p>
            <p class="text-2xl font-bold mt-2">1,248</p>
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
            <p class="text-2xl font-bold mt-2">12</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-yellow-600">⚠️</span>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">近期出入库</p>
            <p class="text-2xl font-bold mt-2">86</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <span class="text-2xl text-purple-600">🔄</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 库存操作 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <div class="bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📥 入库登记</h3>
        <p class="text-gray-600 mb-4">登记新到货物资，更新库存数量</p>
        <button class="px-4 py-2 bg-white border border-blue-500 text-blue-600 rounded-lg hover:bg-blue-50">
          入库登记
        </button>
      </div>
      <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📤 出库申请</h3>
        <p class="text-gray-600 mb-4">申请物资出库，记录领用信息</p>
        <button class="px-4 py-2 bg-white border border-green-500 text-green-600 rounded-lg hover:bg-green-50">
          出库申请
        </button>
      </div>
      <div class="bg-gradient-to-r from-red-50 to-orange-50 rounded-xl p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-3">📊 库存盘点</h3>
        <p class="text-gray-600 mb-4">定期库存盘点，核对实际数量</p>
        <button class="px-4 py-2 bg-white border border-red-500 text-red-600 rounded-lg hover:bg-red-50">
          开始盘点
        </button>
      </div>
    </div>

    <!-- 库存预警列表 -->
    <div class="bg-white rounded-xl shadow overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-bold text-gray-900">库存预警</h2>
        <p class="text-sm text-gray-600">库存低于安全水平的物品</p>
      </div>
      <div class="divide-y divide-gray-200">
        <div v-for="item in lowStockItems" :key="item.id" class="px-6 py-4 flex items-center justify-between">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-gray-200 rounded-lg mr-4"></div>
            <div>
              <h4 class="font-medium text-gray-900">{{ item.name }}</h4>
              <p class="text-sm text-gray-500">{{ item.category }} • {{ item.sku }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-6">
            <div class="text-center">
              <p class="text-sm text-gray-500">当前库存</p>
              <p class="font-bold text-red-600">{{ item.currentStock }}</p>
            </div>
            <div class="text-center">
              <p class="text-sm text-gray-500">安全库存</p>
              <p class="font-medium">{{ item.safetyStock }}</p>
            </div>
            <button class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm">
              采购补货
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const lowStockItems = ref([
  {
    id: 1,
    name: 'A4打印纸',
    category: '办公耗材',
    sku: 'OFF-001',
    currentStock: 120,
    safetyStock: 500
  },
  {
    id: 2,
    name: '黑色墨盒',
    category: '办公耗材',
    sku: 'OFF-002',
    currentStock: 15,
    safetyStock: 50
  },
  {
    id: 3,
    name: '网线（5米）',
    category: '网络设备',
    sku: 'NET-003',
    currentStock: 25,
    safetyStock: 100
  },
  {
    id: 4,
    name: 'USB扩展坞',
    category: '电脑配件',
    sku: 'COM-004',
    currentStock: 8,
    safetyStock: 30
  },
  {
    id: 5,
    name: '办公椅',
    category: '办公家具',
    sku: 'FUR-005',
    currentStock: 5,
    safetyStock: 20
  },
])
</script>