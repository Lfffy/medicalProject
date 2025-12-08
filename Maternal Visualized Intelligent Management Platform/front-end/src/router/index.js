import Vue from 'vue'
import VueRouter from 'vue-router'

// 优化后的核心模块
import Index from '../views/Index.vue'
import Auth from '../views/Auth.vue'
import DataCenter from '../views/DataCenter.vue'
import AnalysisCenter from '../views/AnalysisCenter.vue'
import MonitoringCenter from '../views/MonitoringCenter.vue'
import DashboardCenter from '../views/DashboardCenter.vue'

import MaternalHealthPrediction from '../views/MaternalHealthPrediction.vue'

// 保留原有组件作为备用
import TableData from '../views/TableData.vue'
import AIChat from '../views/AIChat.vue'
import DataEntry from '../views/DataEntry.vue'
import DataImport from '../views/DataImport.vue'
import PrenatalCare from '../views/PrenatalCare.vue'
import FetalMonitoring from '../views/FetalMonitoring.vue'
import NutritionAdvice from '../views/NutritionAdvice.vue'
import WarningSystem from '../views/WarningSystem.vue'

Vue.use(VueRouter)

const routes = [
    // 优化后的主架构路由
    {
        path: '/',
        redirect: '/index'
    },
    {
        path: '/index',
        name: 'Index',
        component: Index,
        meta: { name: '首页' }
    },
    {
        path: '/data-center',
        name: 'DataCenter',
        component: DataCenter,
        meta: { name: '数据中心' }
    },
    {
        path: '/analysis-center',
        name: 'AnalysisCenter',
        component: AnalysisCenter,
        meta: { name: '分析中心' }
    },
    {
        path: '/monitoring-center',
        name: 'MonitoringCenter',
        component: MonitoringCenter,
        meta: { name: '监测中心' }
    },
    {
        path: '/dashboard-center',
        name: 'DashboardCenter',
        component: DashboardCenter,
        meta: { name: '可视化大屏' }
    },
    {
        path: '/maternal-health-prediction',
        name: 'MaternalHealthPrediction',
        component: MaternalHealthPrediction,
        meta: { name: '孕产妇健康预测' }
    },
    
    // 保留原有路由作为备用和兼容性支持

    {
        path: '/tableData',
        name: 'TableData',
        component: TableData,
        meta: { name: "数据表格" }
    },
    {
        path: '/ai-chat',
        name: 'AIChat',
        component: AIChat,
        meta: { name: "AI智能助手" }
    },
    {
        path: '/data-entry',
        name: 'DataEntry',
        component: DataEntry,
        meta: { name: "数据录入" }
    },
    {
        path: '/data-import',
        name: 'DataImport',
        component: DataImport,
        meta: { name: "数据导入" }
    },

    {
        path: '/prenatal-care',
        name: 'PrenatalCare',
        component: PrenatalCare,
        meta: { name: "产检记录" }
    },
    {
        path: '/fetal-monitoring',
        name: 'FetalMonitoring',
        component: FetalMonitoring,
        meta: { name: "胎心监测" }
    },
    {
        path: '/nutrition-advice',
        name: 'NutritionAdvice',
        component: NutritionAdvice,
        meta: { name: "营养建议" }
    },
    {
        path: '/warning-system',
        name: 'WarningSystem',
        component: WarningSystem,
        meta: { name: "预警系统" }
    },

    // 确保所有未匹配的路由都重定向到首页
    {
        path: '*',
        redirect: '/index'
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router