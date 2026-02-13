<template>
  <div id="app" class="h-screen bg-gray-50">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

// 初始化auth store
const authStore = useAuthStore()

onMounted(() => {
  authStore.initialize()
})
</script>

<style>
#app {
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}
</style>