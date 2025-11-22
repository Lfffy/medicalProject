<template>
  <div class="navigation-menu unified-navigation-menu">
    <div class="menu-section">
      <h3 class="menu-title">核心功能</h3>
      <div class="menu-items">
        <router-link to="/data-center" class="menu-item">
          <i class="fas fa-database"></i>
          <span>数据中心</span>
        </router-link>
        <router-link to="/analysis-center" class="menu-item">
          <i class="fas fa-chart-line"></i>
          <span>分析中心</span>
        </router-link>
        <router-link to="/monitoring-center" class="menu-item">
          <i class="fas fa-heartbeat"></i>
          <span>监测中心</span>
        </router-link>
        <router-link to="/dashboard-center" class="menu-item">
          <i class="fas fa-tv"></i>
          <span>可视化大屏</span>
        </router-link>
        <router-link to="/maternal-health-prediction" class="menu-item">
          <i class="fas fa-baby"></i>
          <span>孕产妇健康预测</span>
        </router-link>
      </div>
    </div>
    
    <div class="menu-section">
      <h3 class="menu-title">快速访问</h3>
      <div class="menu-items">
        <router-link to="/ai-chat" class="menu-item">
          <i class="fas fa-robot"></i>
          <span>AI智能助手</span>
        </router-link>
        <router-link to="/tableData" class="menu-item legacy">
          <i class="fas fa-table"></i>
          <span>数据表格</span>
        </router-link>
      </div>
    </div>
    
    <div class="menu-section">
      <h3 class="menu-title">系统管理</h3>
      <div class="menu-items">
        <router-link to="/auth" class="menu-item">
          <i class="fas fa-user-shield"></i>
          <span>认证中心</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavigationMenu',
  methods: {
    handleMenuClick(path) {
      this.$router.push(path);
    }
  }
}
</script>

<style lang="less" scoped>
// 导航菜单组件样式
// 主要样式已在navigation-styles.css中统一定义
// 这里只保留组件特定的样式覆盖

.navigation-menu {
  // 确保导航菜单容器使用统一样式
  background: var(--sidebar-bg);
  border-radius: 15px;
  padding: 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: var(--sidebar-backdrop-filter);
  
  // 确保菜单项高度一致
  .menu-item {
    min-height: var(--menu-item-height);
    display: flex;
    align-items: center;
    
    // 确保图标和文字对齐
    i {
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    span {
      line-height: 1.2;
    }
  }
  
  // 确保菜单标题样式一致
  .menu-title {
    color: #333;
    font-size: var(--menu-title-font-size);
    font-weight: var(--menu-title-font-weight);
    margin-bottom: var(--menu-title-margin-bottom);
    padding-bottom: var(--menu-title-padding-bottom);
    border-bottom: var(--menu-title-border-bottom);
  }
}
</style>