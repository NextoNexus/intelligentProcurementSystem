import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: '登录', public: true }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'suppliers',
        name: 'Suppliers',
        component: () => import('@/views/SuppliersView.vue'),
        meta: { title: '供应商管理' }
      },
      {
        path: 'procurement',
        name: 'Procurement',
        component: () => import('@/views/ProcurementView.vue'),
        meta: { title: '采购管理' }
      },
      {
        path: 'inventory',
        name: 'Inventory',
        component: () => import('@/views/InventoryView.vue'),
        meta: { title: '库存管理' }
      },
      {
        path: 'finance',
        name: 'Finance',
        component: () => import('@/views/FinanceView.vue'),
        meta: { title: '财务管理' }
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: () => import('@/views/AnalyticsView.vue'),
        meta: { title: '报表分析' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/UsersView.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: ':pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/views/NotFoundView.vue'),
        meta: { title: '页面未找到' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫 - 认证检查
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 智能采购系统` : '智能采购系统'

  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isPublic = to.matched.some(record => record.meta.public)

  // 检查用户是否已认证（从localStorage检查token）
  const isAuthenticated = !!localStorage.getItem('access_token')

  if (requiresAuth && !isAuthenticated) {
    // 需要认证但未登录，重定向到登录页面
    next('/login')
  } else if (isPublic && isAuthenticated) {
    // 已登录但访问公开页面（如登录页面），重定向到仪表盘
    next('/dashboard')
  } else {
    // 继续导航
    next()
  }
})

export default router