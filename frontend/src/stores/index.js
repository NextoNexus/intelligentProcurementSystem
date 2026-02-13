import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// 创建pinia实例
const pinia = createPinia()
// 添加持久化插件
pinia.use(piniaPluginPersistedstate)

export default pinia

// 导出所有store
export { useAuthStore } from './auth'
// 后续可以在这里导出其他store
// export { useSuppliersStore } from './suppliers'
// export { useProcurementStore } from './procurement'
// export { useInventoryStore } from './inventory'