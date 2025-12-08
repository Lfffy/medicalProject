<template>
  <div class="unified-layout">
    <Header />
    <div class="main-content">
      <aside class="sidebar unified-sidebar sidebar-width-consistent sidebar-z-index" v-if="showSidebar" :class="{ 'mobile-open': mobileMenuOpen }">
        <NavigationMenu />
      </aside>
      <main class="content-area content-with-sidebar" :class="{ 
        'full-width': !showSidebar,
        'collapsed': !showSidebar 
      }">
        <div class="breadcrumb" v-if="showBreadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-for="(item, index) in breadcrumbItems" :key="index">
              {{ item }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="page-container">
          <router-view />
        </div>
      </main>
    </div>
    
    <!-- 移动端菜单遮罩 -->
    <div class="mobile-overlay" v-if="showSidebar && mobileMenuOpen" @click="closeMobileMenu"></div>
  </div>
</template>

<script>
import Header from './Header.vue'
import NavigationMenu from './NavigationMenu.vue'
import '@/assets/navigation-styles.css'

export default {
  name: 'UnifiedLayout',
  components: {
    Header,
    NavigationMenu
  },
  data() {
    return {
      showSidebar: true,
      showBreadcrumb: true,
      mobileMenuOpen: false
    }
  },
  computed: {
    breadcrumbItems() {
      const route = this.$route
      const meta = route.meta
      return meta && meta.name ? [meta.name] : []
    }
  },
  watch: {
    '$route'(to) {
      // 根据路由控制侧边栏和面包屑显示
      this.updateLayoutSettings(to.path)
      // 路由切换时关闭移动端菜单
      this.closeMobileMenu()
    }
  },
  created() {
    this.updateLayoutSettings(this.$route.path)
    // 监听窗口大小变化
    window.addEventListener('resize', this.handleResize)
    // 监听移动端菜单切换事件
    this.$root.$on('toggle-mobile-menu', this.toggleMobileMenu)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    this.$root.$off('toggle-mobile-menu', this.toggleMobileMenu);
  },
  methods: {
    updateLayoutSettings(path) {
      // 首页和认证页面不显示侧边栏
      this.showSidebar = !['/', '/auth'].includes(path)
      // 首页不显示面包屑
      this.showBreadcrumb = path !== '/'
    },
    handleResize() {
      // 窗口大小变化时关闭移动端菜单
      if (window.innerWidth > 768) {
        this.mobileMenuOpen = false
      }
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    }
  }
}
</script>

<style lang="less" scoped>
.unified-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  
  .main-content {
    display: flex;
    min-height: calc(100vh - 70px);
    position: relative;
    
    .sidebar {
      // 使用统一的CSS变量和样式类
      // 所有样式已在navigation-styles.css中定义
    }
    
    .content-area {
      flex: 1;
      padding: 20px;
      transition: var(--sidebar-transition);
      position: relative;
      margin-left: 0; /* 重置边距 */
      /* 确保内容区域紧贴导航栏 */
      
      &.full-width {
        padding: 0;
        margin-left: 0 !important;
      }
      
      .breadcrumb {
        margin-bottom: 20px;
        padding: 15px 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        
        /deep/ .el-breadcrumb__item {
          .el-breadcrumb__inner {
            color: #666;
            font-weight: 500;
            
            &:hover {
              color: #ff66a3;
            }
          }
          
          &:last-child .el-breadcrumb__inner {
            color: #ff66a3;
            font-weight: 600;
          }
        }
      }
      
      .page-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        min-height: calc(100vh - 200px);
      }
    }
  }
  
  // 移动端遮罩层
  .mobile-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 998;
    display: none;
    
    @media (max-width: 768px) {
      display: block;
    }
  }
}

/* 确保在不同屏幕尺寸下导航栏保持一致 */
@media (max-width: 768px) {
  .unified-layout {
    .main-content {
      .content-area {
        padding: 10px;
        
        .page-container {
          padding: 15px;
          border-radius: 10px;
        }
      }
    }
  }
}

/* 防止内容区域溢出影响导航栏 */
.sidebar-overflow-protection {
  overflow-x: hidden;
}

/* 确保导航栏始终可见 */
.sidebar-visibility-ensure {
  position: relative;
  z-index: 999;
}
</style>